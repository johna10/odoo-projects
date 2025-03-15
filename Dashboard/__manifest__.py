# -*- coding: utf-8 -*-
{
    'name':'DASH',
    'application':True,
    'version': '17.0',
    'author': "Alan John",
    'category': 'Education',
    'summary': 'Summary',
    'data': [
        'security/ir.model.access.csv',
        'views/dashboardComponent_views.xml',
        'views/dashboard_menulist_views.xml',
    ],
'assets': {
        'web.assets_backend': [
            'Dashboard/static/src/js/dashboard.js',
            'Dashboard/static/src/js/dashboard_comments.js',
            'Dashboard/static/src/xml/dashboard.xml',
            'Dashboard/static/src/xml/dashboard_comments.xml',
        ],
    },

}