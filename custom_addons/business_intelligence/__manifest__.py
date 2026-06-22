{
    'name': 'Enterprise Business Intelligence',
    'version': '18.0.2.0.0',
    'category': 'Hidden/Tools',
    'summary': 'Native BI Tools for Sales, Purchase, CRM, Finance, and Inventory',
    'description': """
        Business Intelligence module directly integrated into Odoo.
        Provides a unified dashboard for Analytics using native Odoo Views.
    """,
    'author': 'Arice Project',
    'depends': ['sale_management', 'purchase', 'board', 'crm', 'account', 'stock'],
    'data': [
        'views/analytics_actions.xml',
        'views/dashboard_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
