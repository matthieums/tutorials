# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from . import estate_property_type


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real estate property'
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive'),
    ]

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available from",
        default=fields.Date.add(fields.Date.today(), months=3), copy=False
        )
    expected_price = fields.Float(required=True, copy=False)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'), ('east', 'East'),
            ('west', 'West'), ('south', 'South')
            ]
    )
    state = fields.Selection(
        default='new',
        selection=[
            ('new', 'New'), ('offer received', 'Offer received'),
            ('offer accepted', 'Offer accepted'), ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ]
    )
    property_type_id = fields.Many2one(
        string='Property type',
        comodel_name='estate.property.type'
        )
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many('estate.property.tags', string='Tags')
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute='_compute_total')
    best_price = fields.Float(string="Best offer", compute='_compute_best_price')

    @api.depends('garden_area', 'living_area')
    def _compute_total(self):
        for record in self:
            record.total_area = sum((record.garden_area, record.living_area))

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = False

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sell_property(self):
        for record in self:
            if record.state != 'cancelled':
                for record in self:
                    record.state = 'sold'
                return True
        raise UserError(message="Cannot sell a cancelled property")

    def action_cancel_property(self):
        for record in self:
            if record.state != 'sold':
                for record in self:
                    record.state = 'cancelled'
                return True
        raise UserError(message="Cannot cancel a sold property")

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0.9 * record.expected_price:
                raise ValidationError('Selling price cannot be lower than 90% of expected price')
