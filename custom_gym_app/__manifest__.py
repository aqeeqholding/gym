# -*- coding: utf-8 -*-
{
    'name': "Custom Gym App",
    'summary':
        """
            This module provides the functionality of extensive options for management of Gym.
        """,
    'author': "Fazal Ur Rahman",
    'category': 'Extra Tools',
    'version': '14.0.0.1',
    'depends': ['base', 'planning', 'sale', 'sale_subscription'],

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/gym_registration.xml',
        'views/membership_view.xml',
        'views/schedule_view.xml',
        'reports/report_schedule_card.xml',
        'reports/report_member_card.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
