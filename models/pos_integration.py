from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # Add option to show shoe sizes in POS
    show_shoe_sizes = fields.Boolean(
        string='Show Shoe Sizes in POS',
        default=True,
        help='Display available sizes for shoe products in POS interface'
    )


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """Load shoe variant info to POS"""
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend([
            'shoe_variant_id',
        ])
        return result


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Link back to shoe variant
    shoe_variant_id = fields.Many2one(
        'shoe.product.variant',
        string='Shoe Variant',
        help='Link to shoe variant if this is a shoe product'
    )

    # Display shoe info in product name for POS
    display_name = fields.Char(compute='_compute_display_name_with_shoe_info')

    def _compute_display_name_with_shoe_info(self):
        for product in self:
            if product.shoe_variant_id:
                name = f"{product.name}"
            else:
                name = product.name
            product.display_name = name