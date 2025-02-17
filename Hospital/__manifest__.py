{
    'name':'Hospital',
    'application':True,
    'depends': ['base','hr','hr_hourly_cost'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/hospital_registration_views.xml',
        'views/hospital_op_ticket.xml',
        'views/hospital_consultation.xml',
        'views/hospital_diagnosis.xml',
        'views/hospital_menu.xml',
    ],
}