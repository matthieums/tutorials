# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Type of the property'
    _sql_constraints = [
        ('check_name_is_unique', 'UNIQUE(name)', 'Property name must be unique')
    ]

    name = fields.Char(required=True)
    properties = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id'
        )