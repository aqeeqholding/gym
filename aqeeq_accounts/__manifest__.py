# -*- encoding: utf-8 -*-

{
    'name': 'Al-Aqeeq Accounts',
    'version': '14.0.0.1',
    'author': "Fazal Ur Rahman",
    'category': 'Localization',

    'description':
        """
            This module is developed to handle the requirements that are
            related to the Aqeeq Accounts.
        """,

    'depends': ['account'],

    'data': [
        'data/account_chart_template_data.xml',
        'data/account.group.csv',
        'data/account.account.template.csv',
        'data/l10n_ye_chart_data.xml',
        'data/account_chart_template_configure_data.xml',
    ],
    'post_init_hook': 'load_translations',

    'application': True,
    'installable': True,
    'auto_install': False,
}
