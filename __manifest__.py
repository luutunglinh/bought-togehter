# -*- coding: utf-8 -*-
{
    'name': "Test App",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Myself",
    'website': "http://odoo.website/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'My Project',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/access_token_view.xml',
        'views/shopify_contact_view.xml',
        'views/shopify_order_view.xml',
        'views/shopify_product_view.xml',
        'views/res_config_setting.xml',
        'views/shopify_customize.xml',
        'wizard/wizard_fetch.xml',
        'views/templates.xml',
        'views/bought_widget.xml'

    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'assets': {
        'sample_app.js_package_assets': [
            'sample_app/static/js/index.js',
        ],
    }
}
