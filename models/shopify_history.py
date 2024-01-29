from odoo import fields, models, api

class ShopifyFetch(models.Model):
    _name = "shopify.history"
    _description="Shopify history"
    _order = "create_date desc"

    data = fields.Char()
    name = fields.Char()
    date_from = fields.Date()
    date_to = fields.Date()
    count = fields.Integer()
