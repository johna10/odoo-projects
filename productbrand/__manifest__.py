{
    'name': 'Product Brand',
    'application': True,
    'version': '18.0.1.0.0',
    'author': "Alan John",
    'category': 'Education',
    'summary': 'Show Product Brand in Pos Order Line and Receipt',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_product_form_views.xml',
        'views/product_brand_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'productbrand/static/src/**/*',
        ],
    },
}
# -*- coding: utf-8 -*-
