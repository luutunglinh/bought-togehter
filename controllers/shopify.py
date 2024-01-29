from odoo import http
import werkzeug
import shopify
import traceback
from odoo.http import route, request


class ShopifyAPI(http.Controller):
    @http.route('/test-shopify', auth="public", type='http', csrf=False, cors="*", save_session=False)
    def test_shopify(self, **kwargs):
        api_key = request.env['ir.config_parameter'].sudo().get_param('sample_app.shopify_api_key')
        shared_secret = request.env['ir.config_parameter'].sudo().get_param('sample_app.shopify_secret_key')
        api_version = request.env['ir.config_parameter'].sudo().get_param('sample_app.shopify_api_version')
        shopify.Session.setup(api_key=api_key, secret=shared_secret)

        # create session
        shop_url = kwargs['shop']
        new_session = shopify.Session(shop_url, api_version)

        # redirect to authenticate
        redirect_uri = "https://odoo.website/test-shopify/finalize"
        scopes = ['read_products', 'read_orders']
        auth_url = new_session.create_permission_url(scopes, redirect_uri)
        print('auth_url', auth_url)
        return werkzeug.utils.redirect(auth_url)

    @http.route('/test-shopify/finalize', auth="public", type="http")
    def shopify_finalize(self, **kwargs):
        # setup session

        api_key = request.env['ir.config_parameter'].sudo().get_param('sample_app.shopify_api_key')
        shared_secret = request.env['ir.config_parameter'].sudo().get_param('sample_app.shopify_secret_key')
        api_version = request.env['ir.config_parameter'].sudo().get_param('sample_app.shopify_api_version')

        shopify.Session.setup(api_key=api_key, secret=shared_secret)

        shop_url = kwargs['shop']
        session = shopify.Session(shop_url, api_version)

        access_token = session.request_token(kwargs)

        # Activate session
        session = shopify.Session(shop_url, api_version, access_token)
        shopify.ShopifyResource.activate_session(session)

        address = request.env['ir.config_parameter'].sudo().get_param('sample_app.shopify_ngrok_url')

        webhook = shopify.Webhook.find()
        print(webhook, 'webhook')

        for w in webhook:
            print('w', w.address)
            if not w.address.split('/test-shopify')[0] == address:
                shopify.Webhook.destroy(w)

        topic = 'products'
        events = ['create', 'update', 'delete']
        self.create_hook(self, address, shop_url, topic, events)

        topic = 'orders'
        events = ['create', 'updated', 'edited', 'cancelled']
        self.create_hook(self, address, shop_url, topic, events)

        for wh in shopify.Webhook.find():
            print(f'''
                     -----------------------------------------
                                   topic: {wh.topic}
                                   address: {wh.address}
                                   private_metafield_namespaces: {wh.private_metafield_namespaces}
                              ''')
        model = request.env['access.token']
        record = model.sudo().search([('shop_url','=',shop_url)])

        if not record:
            shop = shopify.Shop.current()
            data = record.sudo().create({
                'name': shop.name,
                'shop_url': shop.myshopify_domain,
                'access_token': access_token,
                'email': shop.email,
                'country_code': shop.country_code,
                'country_name': shop.country_name,
                'currency': shop.currency
            })
            at_id = data.id
        else:
            at_id = record.id
            record.sudo().write({
                'access_token': access_token
            })
        return request.redirect('/')


    @staticmethod
    def create_hook(self, address, shop_url, topic, events):
        for e in events:
            hook = self.get_hook(address, shop_url, topic, e)
            shopify.Webhook.create(hook)

    @staticmethod
    def get_hook(address, shop_url, topic, method):
        return {
            'topic': f'{topic}/{method}',
            'address': f'{address}/test-shopify/{shop_url}/{topic}/{method}',
            'format': 'json'
        }
