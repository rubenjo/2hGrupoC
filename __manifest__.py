# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Infraestructuras',
    'version': '2.0',
	'author': 'Jorge Blasco Repollés',
    'category': 'Human Resources',
    'sequence': 105,
    'summary': 'Cesión de infraestructuras a terceros',
    'description': """
Infraestructuras
============================

Esta aplicación te permite gestionar la cesión de infraestructuras a terceros.

    """,
    'website': 'http://www.iamz.ciheam.org/es/',
    'depends': ['hr', 'calendar', 'resource', 'report'],
    'data': [
        'views/hr_infraestructuras_view.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'data/hr_infraestructuras_groups.xml',
        ],
    'installable': True,
    'application': True,
}
