{
    'name': 'Clear Cart',
    'application': True,
    'version': '18.0.1.0.0',
    'author': "Alan John",
    'category': 'Education',
    'summary': 'THIS IS UPDATED',
    'depends': ['website', 'sale', 'website_payment', 'website_mail', 'portal_rating', 'digest', 'delivery','website_sale'],
    'data': [
        'views/website_ecommerce_clear_cart.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'clearcart/static/src/js/clear_cart.js',
        ],
    },
}
# -*- coding: utf-8 -*-
