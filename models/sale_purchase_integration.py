from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    shoe_variant_id = fields.Many2one(
        'shoe.product.variant',
        string='Shoe Variant',
        compute='_compute_shoe_variant',
        store=True
    )
    shoe_size = fields.Many2one(
        'shoe.size',
        string='Size',
        related='shoe_variant_id.size_id',
        store=True,
        readonly=True
    )

    shoe_color = fields.Many2one(
        'shoe.color',
        string='Color',
        related='shoe_variant_id.color_id',
        store=True,
        readonly=True
    )

    @api.depends('product_id')
    def _compute_shoe_variant(self):
        for line in self:
            if line.product_id and line.product_id.shoe_variant_id:
                line.shoe_variant_id = line.product_id.shoe_variant_id
            else:
                line.shoe_variant_id = False


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    shoe_variant_id = fields.Many2one(
        'shoe.product.variant',
        string='Shoe Variant',
        compute='_compute_shoe_variant',
        store=True
    )
    shoe_size = fields.Char(
        string='Size',
        related='shoe_variant_id.size_id.name',
        store=True
    )
    shoe_color = fields.Char(
        string='Color',
        related='shoe_variant_id.color_id.name',
        store=True
    )

    @api.depends('product_id')
    def _compute_shoe_variant(self):
        for line in self:
            if line.product_id and line.product_id.shoe_variant_id:
                line.shoe_variant_id = line.product_id.shoe_variant_id
            else:
                line.shoe_variant_id = False