# -*- coding: utf-8 -*-
{
    'name':'4 My Study',
    'application':True,
    'version': '18.0.1.0.0',
    'author': "Alan John",
    'category': 'Sales',
    'summary': 'Add a new field to the Invoice',
    'depends': ['mail','base','sale_management','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/delegation_keyboard_views.xml',
        'views/delegation_screen_views.xml',
        'views/delegation_laptop_views.xml',
        'views/delegation_menu_views.xml',
    ],
}