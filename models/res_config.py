
from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    shopify_api_key = fields.Char('API Key', config_parameter= 'sample_app.shopify_api_key')
    shopify_secret_key = fields.Char('API Secret', config_parameter= 'sample_app.shopify_secret_key')
    shopify_api_version = fields.Char('API Version', config_parameter= 'sample_app.shopify_api_version')
    shopipy_ngrok_url = fields.Char('Ngrok URL', config_parameter= 'sample_app.shopify_ngrok_url')
    xero_client_id = fields.Char('Client ID', config_parameter= 'sample_app.xero_client_id')
    xero_client_secret = fields.Char('Client Secret', config_parameter= 'sample_app.xero_client_secret')


