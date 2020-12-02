# -*- coding: utf-8 -*-

{
    'name': 'Portal Page Design',
    'version': '1.0',
    'category': 'Website',
    'summary': """
                    Design the portal page in card dashboard like view
               """,
    'author': "Fazal Ur Rahman",
    'license': 'LGPL-3',
    'depends': ['website'],

    'data': [
                'views/assets.xml',
                'views/portal.xml',
            ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
