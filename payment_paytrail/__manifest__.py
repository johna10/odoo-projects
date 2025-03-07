# -*- coding: utf-8 -*-
{
    'name': 'Payment Provider - Paytrail',
    'application': True,
    'version': '18.0.1.0.0',
    'author': "Alan John",
    'category': 'Education',
    'summary': 'Add Paytrail payment provider to odoo',
    'depends': ['payment'],
    'data': [
        'views/payment_provider_views.xml',

        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',

    ],

}

