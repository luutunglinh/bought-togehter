from odoo import http
from odoo.http import route, request, Response

class ProductController(http.Controller):
    @http.route('/test-shopify/<string:shop_url>/products/create', auth='public', type='json')
    def shopify_product_create(self, shop_url):
        val = request.jsonrequest
        model = request.env['shopify.product']
        shop = request.env['access.token'].sudo().search([('shop_url','=',shop_url)])

        model.sudo().create({
            'product_id': val['id'],
            'name': val['title'],
            'price': val['variants'][0]['price'],
            'compare': val['variants'][0]['compare_at_price'],
            'quantity': val['variants'][0]['inventory_quantity'],
            'shop_id': shop.id
        })

        return  Response("success", status=200)

    @http.route('/test-shopify/<string:shop_url>/products/update', auth='public', type='json')
    def shopify_product_update(self, shop_url):
        val = request.jsonrequest
        print(val['id'])
        shop = request.env['access.token'].sudo().search([('shop_url','=',shop_url)])
        product = request.env['shopify.product'].sudo().search([('product_id','=',val['id']),('shop_id','=',shop.id)])

        if product:
            product.sudo().write({
                'name': val['title'],
                'price': val['variants'][0]['price'],
                'compare': val['variants'][0]['compare_at_price'],
                'quantity': val['variants'][0]['inventory_quantity'],
            })
        print('update', product.name)
        return Response("success", status=200)

    @http.route('/test-shopify/<string:shop_url>/products/delete', auth='public', type='json')
    def shopify_product_delete(self,shop_url):
        val = request.jsonrequest
        shop = request.env['access.shopify'].sudo().search([('shop_url', '=', shop_url)])
        product = request.env['shopify.product'].sudo().search([('product_id','=',val['id']),('shop_id','=',shop.id)])
        if product:
            product.sudo().unlink()
        return Response("success", status=200)


