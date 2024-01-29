import werkzeug
from odoo import http
from odoo.http import request, route, Response
import json
import shopify
import re


class SampleApp(http.Controller):
    @http.route(['/dashboard/<string:name>',
                 '/dashboard/store/<string:name>'], auth='user', type='http')
    def dashboard_bought_together(self, **kwargs):
        current_uid = request.env.context.get('uid')
        cur_user = request.env['res.users'].browse(current_uid)
        print(cur_user)
        model_token = request.env['access.token'].search([])
        widget_model = request.env['bought.widget']
        stores = []

        for item in model_token:
            print(item.id)
            wgs = widget_model.sudo().search([('shop_id', '=', item.id)])
            included = 0
            for wg in wgs:
                included += len(wg.product_ids)
            stores.append({
                'key': item.shop_url.split(".myshopify.com")[0],
                'name': item.name,
                'product_included': included,
                'status': item.status
            })
            print(stores)
        value = {
            'user_name': cur_user.name,
            "id": cur_user.id,
            'user_image': cur_user.image_1920.decode('utf-8'),
            'stores': stores,
        }

        return request.render('sample_app.sample_app_template', {'app_settings': json.dumps(value)})

    # store
    @http.route('/sample-app/store-status', type='json', auth='public')
    def change_store_status(self, store, status):
        shop = request.env['access.token'].sudo().search([('name', '=', store)])
        if shop:
            shop.status = status
        return shop.status

    @http.route('/sample-app/get-data-store', type='json', auth="public")
    def get_data_store(self, name):
        data_recommend_table = self.get_widget_products(name, 'recommendation')
        data_excluded_table = self.get_widget_products(name, 'excluded')
        store_status = request.env['access.token'].sudo().search([('name', '=', name)]).status

        value = {
            'store': name,
            'store_status': store_status,
            'dataRecommendTable': data_recommend_table,
            'dataExcludedTable': data_excluded_table,
        }
        return value

    @http.route('/sample-app/search-product', type='json', auth="public")
    def search_product(self, searchText, shop):
        model = request.env['access.token'].sudo().search([('name', '=', shop)])
        access_token = model.access_token
        shop_url = f'{shop}.myshopify.com'
        api_version = request.env['ir.config_parameter'].sudo().get_param('sample_app.shopify_api_version')
        session = shopify.Session(shop_url, api_version, access_token)
        shopify.ShopifyResource.activate_session(session)
        print(searchText, shop)

        graphQL1 = """
                               query {
                                     productVariants(first: 5"""
        graphQL2 = """) {
                                       edges {
                                          node {
                                            id
                                            displayName
                                            price
                                            compareAtPrice
                                            inventoryQuantity
                                            product {
                                              title
                                              featuredImage {
                                                url
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                           """

        if searchText:
            variables = f', query: "title: {searchText}"'  # Tìm kiếm theo tiêu đề
            result = shopify.GraphQL().execute(graphQL1 + variables + graphQL2)
            return json.loads(result)['data']['productVariants']['edges']
        else:
            result = shopify.GraphQL().execute(graphQL1 + graphQL2)

            return json.loads(result)['data']['productVariants']['edges']

    @staticmethod
    def get_widget_products(name, type):
        data = []
        shop = request.env['access.token'].sudo().search([('name', '=', name)])
        if shop:
            widget = request.env['bought.widget'].search([('shop_id', '=', shop.id), ('type', '=', type)])
            if widget:
                for w in widget.product_ids:
                    data.append({
                        "key": w.product_id,
                        "title": w.name,
                        "url": w.url,
                        "price": w.price,
                        "compare": w.compare,
                        "quantity": w.quantity,
                    })
        return data

    @http.route("/sample-app/save-product", auth="public", type="json")
    def save_product(self, shop, type, data):
        print('datadadaaad', data)
        access_token = request.env['access.token'].sudo().search([("name", '=', shop)])
        shop_id = access_token.id
        shop_product_model = request.env['shopify.product']
        bt_widget_model = request.env['bought.widget']
        product_ids = []
        for item in data:
            product = shop_product_model.search([('product_id', '=', item['key']), ('shop_id', '=', shop_id)])
            if not product:
                product = shop_product_model.sudo().create({
                    'name': item['title'],
                    'price': item['price'],
                    'product_id': item['key'],
                    'url': item['url'],
                    'compare': item['compare'],
                    'quantity': item['quantity'],
                    'shop_id': shop_id,
                })
            product_ids.append(product.id)
        widget_data = bt_widget_model.search([('shop_id', '=', shop_id), ('type', '=', type)])
        if not widget_data:
            bt_widget_model.sudo().create({
                'shop_id': shop_id,
                'product_ids': product_ids,
                'type': type,
            })
        else:
            widget_data.sudo().write({
                'product_ids': product_ids,
            })
        return Response("success", status=200)

    @http.route('/sample-app/get_widget_data', auth="public", type="json")
    def get_widget_data(self, shop, shop_id, type):
        print(shop, shop_id, type)
        data = []
        bt_widget_model = request.env['bought.widget']
        widget_data = bt_widget_model.sudo().search([('shop_id', '=', shop_id), ('type', '=', type)])
        if widget_data:
            for w in widget_data.product_ids:
                data.append({
                    "key": w.product_id,
                    "name": w.name,
                    "url": w.url,
                    "price": w.price,
                    "compare": w.compare,
                    "url": w.url,
                    "quantity": w.quantity,
                })
        return data

    @http.route('/sample-app/save_customization', auth="public", type="json")
    def save_products_customization(self, name, data, user_id):
        print('kw', name)
        print(data)
        customize_setting = request.env['shopify.customize'].sudo().search([("user_id", '=', user_id)])
        if not customize_setting:
            customize_setting.sudo().create({
                'user_id': user_id,
                'customization_setting': data,
            })
        else:
            customize_setting.sudo().write({
                'customization_setting': data,
            })

    @http.route('/sample-app/get_customization', auth="public", type="json")
    def get_products_customization(self, user_id):
        print(user_id)
        customize_setting = request.env['shopify.customize'].sudo().search([("user_id", '=', user_id)])
        if customize_setting:
            print(customize_setting.customization_setting)
            customize_shop = customize_setting.customization_setting
            return customize_shop
