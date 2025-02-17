# -*- coding: utf-8 -*-
{
    'name':'Invoice For Multiple Sale Order',
    'application':True,
    'version': '18.0.1.0.0',
    'author': "Alan John",
    'category': 'Sales',
    'summary': 'Add a new field to the Invoice',
    'depends': ['mail','base','sale_management','contacts'],
    'data': [
        'views/account_move_views.xml',
    ],
}