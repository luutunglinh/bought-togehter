from odoo import fields, models, api

class ShopifyContact(models.Model):
    _name = 'shopify.contact'
    _description = 'shopify contact'

    shopify_contact_id = fields.Char('Shopify Contact ID')
    name = fields.Char('Name')
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    shop_id = fields.Char('Shopify Shop ID')
    xero_contact_id = fields.Char("Xero contact id")