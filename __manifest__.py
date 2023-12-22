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
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',

        'data/ir_sequence_cloth.xml',

        'views/cloth_order_views.xml',
        'views/customer_views.xml',
        'views/product_management_views.xml',
        'views/invoice_views.xml',
        'views/product_template_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
