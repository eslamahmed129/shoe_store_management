# models/shoe_color.py
from odoo import models, fields

class ShoeColor(models.Model):
    _name = 'shoe.color'
    _description = 'Shoe Color'

    name = fields.Char(string='Color Name', required=True)
    code = fields.Char(string='Color Code', help='HTML Color Code')
    active = fields.Boolean(default=True)