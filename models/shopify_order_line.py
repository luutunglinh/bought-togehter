from odoo import fields, models, api

class ShopifyOrderLine(models.Model):
    _name = "shopify.order.line"
    _description = 'Shopify Order Line'

    order_id = fields.Many2one('shopify.order', string="Order id")
    product_id = fields.Many2one('shopify.product', string=" Product")
    quantity = fields.Integer("Quantity", default=1)
    unit_amount = fields.Integer(string='Unit Amount', related='product_id.price', store=True)
    account_code = fields.Char(string='Account Code', default='200')
    line_amount = fields.Integer(string='Line Amount', compute='_compute_amount', store=True)
    line_item_id = fields.Char(string='Line Item ID')

    @api.depends('quantity', 'unit_amount')
    def _compute_amount(self):
        for item in self:
            item.line_amount = item.unit_amount * item.quantity

