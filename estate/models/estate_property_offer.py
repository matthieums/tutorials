# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class Offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer from a buyer'

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'), ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity(days)")
    date_deadline = fields.Date(computed='_compute_deadline', inverse='_inverse_deadline', string='Deadline')

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date, days=record.validity
                )

    # If someone edits the deadline manually, the validity should be updated
    def _inverse_deadline(self):
        for record in self:
            deadline_date = fields.Date.from_string(record.date_deadline)
            create_date = fields.Datetime.from_string(record.create_date)
            delta = deadline_date - create_date.date()
            record.validity = delta.days
    