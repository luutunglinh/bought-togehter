from odoo import fields, models, api


class Widget(models.Model):
    _name = 'bought.widget'
    _description = 'Product of Bought Together'

    shop_id = fields.Char('Shop')
    product_ids = fields.Many2many('shopify.product', string='Product in widget')
    type = fields.Char('Type')