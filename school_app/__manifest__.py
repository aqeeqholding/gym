# -*- coding: utf-8 -*-
{
    'name': "School App",

    'summary': """
        This module is developed to manage the requirements related to
        the School Management System.""",

    'description': """
        This module is developed to manage the requirements related to
        the School Management System
    """,

    'author': "Fazal Ur Rahman",
    'category': 'Extra Tools',
    'version': '14.0.0.1',
    'depends': ['base', 'contacts', 'website'],

    'data': [
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
