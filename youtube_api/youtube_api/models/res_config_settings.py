from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    google_client_id = fields.Char("Client ID", config_parameter='youtube_api.google_client_secret')
    google_client_secret = fields.Char("Clien Secret", config_parameter = 'youtube_api.google_client_secret')
