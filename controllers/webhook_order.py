from odoo import http
from odoo.http import route, request, Response
import shopify


class OrdersController(http.Controller):

    @http.route('/test-shopify/<string:shop_url>/orders/create', auth='public', type='json')
    def test_shopify_orders_create(self, shop_url):
        val = request.jsonrequest
        contact_model = request.env['shopify.contact']
        order_model = request.env['shopify.order']
        product_model = request.env['shopify.product']
        shop_model = request.env['access.token'].sudo().search([('shop_url', '=', shop_url)])
        order_line_model = request.env['shopify.order.line']

        order_line_ids = []
        for line_item in val['line_items']:
            product = product_model.sudo().search([('product_id', '=', line_item['product_id']),
                                                   ('shop_id', '=', shop_model.id)
                                                   ])
            if not product:
                product = product_model.sudo().create({
                    'product_id': line_item['product_id'],
                    'name': line_item['name'],
                    'price': line_item['price'],
                    'shop_id': shop_model.id
                })

            order_line = order_line_model.sudo().create({
                'product_id': product.id,
                'quantity': line_item['quantity'],
                'unit_amount': product.price,
                'line_item_id': line_item['id']
            })
            order_line_ids.append(order_line.id)

        contact = contact_model.sudo().search([('shopify_contact_id', '=', val['customer']['id']),
                                               ('shop_id', '=', shop_model.id)
                                               ])
        if not contact:
            contact = contact_model.sudo().create({
                'shopify_contact_id': val['customer']['id'],
                'name': f"{val['customer']['first_name']} {val['customer']['last_name']}",
                'phone': val['customer']['phone'],
                'email': val['customer']['email'],
                'shop_id': shop_model.id
            })
        if order_line_ids and contact:
            order = order_model.sudo().create({
                'order_id': val['id'],
                'shop_id': shop_model.id,
                'name': val['name'],
                'contact': contact.id,
                'order_line_ids': [(6, 0, order_line_ids)],
                'financial_status': val['financial_status'],
                'date': val['updated_at']
            })
        return Response("success", status=200)

    @http.route('/test-shopify/<string:shop_url>/orders/updated', auth='public', type='json')
    def test_shopify_orders_update(self, shop_url):

        val = request.jsonrequest
        product_model = request.env['shopify.product']
        shop_model = (request.env['access.token'].sudo().search([('shop_url', '=', shop_url)]))
        order_line_model = request.env['shopify.order.line']
        order_model = (request.env['shopify.order'].
                       sudo().search([('order_id', '=', val['id']), ('shop_id', '=', shop_model.id)])
                       )
        order_line_ids = []
        if order_model and val['line_items']:
            for line_item in val['line_items']:
                print(line_item)
                order_line = order_line_model.sudo().search([('line_item_id', '=', line_item['id'])])
                if order_line:
                    ## route updated cho phần fullfillitem
                    order_line.write({
                        'quantity': line_item['quantity']
                    })
                else:
                    product = product_model.sudo().search([('product_id', '=', line_item['product_id']),
                                                           ('shop_id', '=', shop_model.id)])
                    if not product:
                        product = product_model.sudo().create({
                            'product_id': line_item['product_id'],
                            'name': line_item['name'],
                            'price': line_item['price'],
                            'shop_id': shop_model.id
                        })
                    ##add những sản phẩm vào order khi updated
                    order_line = order_line_model.sudo().create({
                        'product_id': product.id,
                        'quantity': line_item['quantity'],
                        'unit_amount': product.price,
                        'line_item_id': line_item['id']
                    })
                order_line_ids.append(order_line.id)

            order_model.sudo().write({
                'name': val['name'],
                'order_line_ids': [(6, 0, order_line_ids)],
                'financial_status': val['financial_status'],
                'date': val['updated_at']
            })
        return Response("success", status=200)

    @http.route('/test-shopify/<string:shop_url>/orders/cancelled', auth='public', type='json')
    def shopify_orders_cancelled(self, shop_url):
        val = request.jsonrequest
        shop_model = request.env['access.token'].sudo().search([('shop_url', '=', shop_url)])
        order_model = (request.env['shopify.order'].sudo()
                       .search([('order_id', '=', val['id']), ('shop_id', '=', shop_model.id)
                                ])
                       )
        if order_model:
            order_model.sudo().unlink()

        return Response("success", status=200)
