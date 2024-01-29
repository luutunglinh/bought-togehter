import werkzeug
from odoo import fields, models, api


class AccessToken(models.Model):
    _name = 'access.token'
    _description =  'Access token'

    name = fields.Char("Name Shop", compute='_compute_name_shop', store = True)
    shop_url = fields.Char('Shop url')
    access_token = fields.Char('Access Token')
    email = fields.Char('Email')
    country_code = fields.Char('Country Code')
    country_name = fields.Char('Country Name')
    currency = fields.Char('Currency')
    status = fields.Boolean(string='Shop Status', default=True)
    customization_setting = fields.Text(string="Customization")

    @api.depends('shop_url')
    def _compute_name_shop(self):
        for record in self:
            record.name = record.shop_url.split(".myshopify.com")[0]

    def redirect_home(self):
        url = f"https://admin.shopify.com/store/{self.shop_url.split('.')[0]}"
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url
        }

    def connect_xero(self):
        print("test")
