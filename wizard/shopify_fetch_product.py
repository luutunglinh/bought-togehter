from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime
import shopify


class FetchProduct(models.TransientModel):
    _name = "fetch.product.wizard"
    _description = "fetch products from shopify"

    data_selection = fields.Selection([
        ('products', 'Products'),
        ('orders', 'Orders')
    ], string='Selection Fetch')
    shop_id = fields.Many2one('access.token', string="Shop")

    date_from = fields.Date("Date from")
    date_to = fields.Date("Date to")

    @api.constrains('date_from', 'date_to')
    def constrains_date(self):
        for rec in self:
            if rec.date_from > rec.date_to:
                raise ValidationError("Stat date is not  more than end date")

    def fetch_shopify(self):
        api_version = self.env['ir.config_parameter'].sudo().get_param('sample_app.shopify_api_version')
        session = shopify.Session(self.shop_id.shop_url, api_version, self.shop_id.access_token)
        shopify.ShopifyResource.activate_session(session)
        date_from = self.date_from.strftime("%Y-%m-%d")
        date_to = self.date_to.strftime("%Y-%m-%d")
        count_fetch = 0

        if self.data_selection == 'products':
            type = 'products'
            products = shopify.Product.find(updated_at_min=date_from, update_at_max=date_to)
            model = self.env['shopify.product']
            for item in products:
                if not model.search([('product_id', '=', item.id), ('shop_id', '=', self.shop_id.id)]):
                    model.sudo().create({
                        'product_id': item.id,
                        'name': item.title,
                        'price': item.variants[0].price,
                        'compare': item.variants[0].compare_at_price,
                        'quantity': item.variants[0].inventory_quantity,
                        'shop_id': self.shop_id.id
                    })
                    count_fetch += 1
                    print(count_fetch)
        if self.data_selection == 'orders':
            type = 'orders'
            orders = shopify.Order.find(updated_at_min=date_from, update_at_max=date_to, status='any')
            model_product = self.env['shopify.product']
            model_order = self.env['shopify.order']
            model_order_line = self.env['shopify.order.line']
            contact_model = self.env['shopify.contact']
            order_line_id = []
            for o in orders:
                if not model_order.search([('order_id', '=', o.id), ('shop_id', '=', self.shop_id.id)]):
                    if o.customer is not None and o.line_items is not None:
                        # if item.line_items:
                        for line_item in o.line_items:
                            product = model_product.search([('product_id', '=', line_item.product_id),
                                                            ('shop_id', '=', self.shop_id.id)])
                            if not product:
                                product = model_product.sudo().create({
                                    'product_id': line_item.product_id,
                                    'name': line_item.title,
                                    'price': line_item.price,
                                    'compare':line_item.compare,
                                    'quantity': line_item.quantity,
                                    'shop_id': self.shop_id.id
                                })
                            order_line = model_order_line.create({
                                'product_id': product.id,
                                'quantity': line_item.quantity,
                                'unit_amount': product.price,
                                'line_item_id': line_item.id,
                            })
                            order_line_id.append(order_line.id)
                        contact = contact_model.search([('shopify_contact_id', '=', o.customer.id),
                                                        ('shop_id', '=', self.shop_id.id)])
                        if not contact:
                            contact = contact_model.create({
                                'shopify_contact_id': o.customer.id,
                                'name': f'{o.customer.first_name} {o.customer.last_name}',
                                'phone': o.customer.email,
                                'email': o.customer.phone,
                                'shop_id': self.shop_id.id
                            })
                        model_order.sudo().create({
                            'order_id': o.id,
                            'shop_id': self.shop_id.id,
                            'name': o.name,
                            'order_line_ids': order_line_id,
                            'financial_status': o.financial_status,
                            'date': o.updated_at
                        })
                        count_fetch += 1

        if count_fetch:
            self.env['shopify.history'].create({
                'data': type,
                'name': self.shop_id.name,
                'date_from': date_from,
                'date_to': date_to,
                'count': count_fetch
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': f'fetch success {count_fetch} item',
                'type': 'success',
                'sticky': False,
            }
        }
