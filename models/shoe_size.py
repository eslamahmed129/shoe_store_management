# models/shoe_size.py
from odoo import models, fields, api

class ShoeSize(models.Model):
    _name = 'shoe.size'
    _description = 'Shoe Size'
    _order = 'sequence, name'

    name = fields.Char(string='Size', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    eu_size = fields.Float(string='EU Size')
    us_size = fields.Float(string='US Size')
    uk_size = fields.Float(string='UK Size')
    cm_size = fields.Float(string='CM Size')
    active = fields.Boolean(default=True)