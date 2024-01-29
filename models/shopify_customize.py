from odoo import models, fields

class ShopifyCustomize(models.Model):
    _name = "shopify.customize"
    _description = "Shopify Customization"

    name= fields.Char("Test")
    user_id = fields.Many2one('res.users', string="User_id")
    customization_setting = fields.Text("Customization Settings")
