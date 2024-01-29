from odoo import fields, models, api

class ShopifyOrder(models.Model):
    _name = 'shopify.order'
    _description = 'shopify order'

    order_id = fields.Char('Shopify order id')
    shop_id = fields.Many2one('access.token', string='Shop url')
    name = fields.Char('Order Name')
    order_line_ids = fields.One2many('shopify.order.line',
                                     'order_id', string='Order line')
    date = fields.Date('Order date')
    financial_status = fields.Char('Order Status')
    xero_invoice_ids = fields.Char("Xero Invoice ID")
    contact = fields.Many2one('shopify.contact', string='Contact')