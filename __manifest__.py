# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Rental System",
    'version': '16.0.0.0.1',
    'summary': 'Cloth Rental System',
    'author': 'Ramiz Belim',
    'sequence': 10,
    'description': """ Cloth Rental System """,
    'category': 'Inventory',
    'depends': ['sale_management', 'mail', 'website_profile'],
    'data': [
        'security/ir.model.access.csv',
        'security/cloth_rental_security.xml',
        'security/ir_rule.xml',

        'wizard/assigned_order_wizard_views.xml',
        'wizard/assigned_order_force_wizard_views.xml',
        'wizard/error_message_wizard_views.xml',

        # 'report/ir_actions_report_templates.xml',
        'report/ir_actions_report.xml',
        'report/sale_order_report.xml',
        'report/custom_report.xml',

        'data/ir_sequence_cloth.xml',
        'data/mail_template_data.xml',
        'data/mail_template_order.xml',
        'data/ir_cron_data.xml',
        'data/ir_actions_data.xml',

        'views/cloth_order_views.xml',
        'views/customer_views.xml',
        'views/product_management_views.xml',
        'views/invoice_views.xml',
        'views/product_template_views.xml',
        'views/cloth_washing_views.xml',
        'views/menu_views.xml',
        'views/website_views.xml',
        'views/website_dynamic_views.xml',
        'views/website_rental_customer_views.xml',
        'views/controller_override_views.xml',
        'views/static_snippets.xml',
        'views/web_rental_products_snippet.xml',
        'views/form_cloth_washing.xml'
    ],
    'assets': {
        'rental_system.assets_frontend': [
            'rental_system/static/src/scss/controller_override.scss'
        ]},
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
