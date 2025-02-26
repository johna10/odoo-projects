{
    'name': 'Pos Discount Limit',
    'application': True,
    'version': '18.0.1.0.0',
    'author': "Alan John",
    'category': 'Education',
    'summary': 'Add discount limit for each session',
    'depends': ['point_of_sale'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_discount_limit/static/src/**/*',
        ],
    },
}
# -*- coding: utf-8 -*-
