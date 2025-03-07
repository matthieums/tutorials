# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class EstateTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Tags for properties'
    _sql_constraints = [
        ('check_tag_is_unique', 'UNIQUE(name)', 'Tag names must be unique')
    ]

    name = fields.Char(required=True)
