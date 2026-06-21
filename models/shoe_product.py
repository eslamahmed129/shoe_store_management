from odoo import models, fields, api


class ShoeProductVariant(models.Model):
    """Define Variant first before ShoeProduct"""
    _name = 'shoe.product.variant'
    _description = 'Shoe Product Variant'
    _rec_name = 'display_name'

    shoe_product_id = fields.Many2one('shoe.product', string='Shoe Product',
                                      required=True, ondelete='cascade')
    size_id = fields.Many2one('shoe.size', string='Size', required=True)
    color_id = fields.Many2one('shoe.color', string='Color', required=True)

    # Link to Odoo Product
    product_id = fields.Many2one('product.product', string='Odoo Product')

    # Stock
    qty_available = fields.Float(related='product_id.qty_available',
                                 string='Quantity On Hand', readonly=True)
    virtual_available = fields.Float(related='product_id.virtual_available',
                                     string='Forecast Quantity', readonly=True)

    # Pricing
    list_price = fields.Float(string='Sale Price')
    standard_price = fields.Float(string='Cost Price')

    # Barcode
    barcode = fields.Char(string='Barcode', related='product_id.barcode')

    display_name = fields.Char(compute='_compute_display_name', store=True)

    active = fields.Boolean(default=True)

    # # Inside ShoeProduct class, add:
    #
    # total_qty_available = fields.Float(
    #     string='Total Quantity On Hand',
    #     compute='_compute_total_quantities'
    # )
    # total_virtual_available = fields.Float(
    #     string='Total Forecast Quantity',
    #     compute='_compute_total_quantities'
    # )
    #
    # @api.depends(
    #     'shoe_product_id.variant_ids.qty_available',
    #     'shoe_product_id.variant_ids.virtual_available'
    # )
    # def _compute_total_quantities(self):
    #     for record in self:
    #         variants = record.shoe_product_id.variant_ids
    #         record.total_qty_available = sum(variants.mapped('qty_available'))
    #         record.total_virtual_available = sum(variants.mapped('virtual_available'))

    @api.depends('shoe_product_id.name', 'size_id.name', 'color_id.name')
    def _compute_display_name(self):
        for record in self:
            if record.shoe_product_id and record.size_id and record.color_id:
                record.display_name = f"{record.shoe_product_id.name} - " \
                                      f"Size {record.size_id.name} - " \
                                      f"{record.color_id.name}"
            else:
                record.display_name = 'New Variant'

    @api.model_create_multi
    def create(self, vals_list):
        """Create corresponding product.product when variant is created"""
        variants = super().create(vals_list)

        for variant in variants:
            if not variant.product_id:
                # Create the product name
                product_name = variant.display_name

                # Create default code
                default_code = ""
                if variant.shoe_product_id.default_code:
                    default_code = f"{variant.shoe_product_id.default_code}-"
                default_code += f"{variant.size_id.name}-{variant.color_id.name}"

                # Inside ShoeProductVariant.create() method
                # بعد ما تعمل create للـ product، ضيف السطر ده:

                product = self.env['product.product'].create({
                    'name': product_name,
                    'default_code': default_code,
                    'list_price': variant.list_price,
                    'standard_price': variant.standard_price,
                    'categ_id': variant.shoe_product_id.categ_id.id if variant.shoe_product_id.categ_id else False,
                    'type': 'product',
                    'tracking': 'none',
                    'available_in_pos': True,  # ✅ Add this
                })
                variant.product_id = product.id
                product.shoe_variant_id = variant.id  # ✅ Add this - Link back

        return variants


class ShoeProduct(models.Model):
    """Define ShoeProduct after Variant"""
    _name = 'shoe.product'
    _description = 'Shoe Product'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Product Name', required=True, tracking=True)
    default_code = fields.Char(string='Internal Reference')
    categ_id = fields.Many2one('product.category', string='Category')
    brand = fields.Char(string='Brand')
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('all_season', 'All Season')
    ], string='Season', default='all_season')

    # Gender
    gender = fields.Selection([
        ('men', 'Men'),
        ('women', 'Women'),
        ('kids', 'Kids'),
        ('unisex', 'Unisex')
    ], string='Gender', required=True)

    # Price
    list_price = fields.Float(string='Sale Price', required=True, default=0.0)
    standard_price = fields.Float(string='Cost Price', default=0.0)

    # Sizes and Colors
    size_ids = fields.Many2many('shoe.size', string='Available Sizes')
    color_ids = fields.Many2many('shoe.color', string='Available Colors')

    # Variants - NOW this will work because ShoeProductVariant is defined above
    variant_ids = fields.One2many('shoe.product.variant', 'shoe_product_id',
                                  string='Variants')
    variant_count = fields.Integer(compute='_compute_variant_count',
                                   string='Variant Count')

    # Images
    image_1920 = fields.Image(string='Image', max_width=1920, max_height=1920)

    # Description
    description = fields.Text(string='Description')

    active = fields.Boolean(default=True)
    total_qty_available = fields.Float(
        string='Total Quantity On Hand',
        compute='_compute_total_quantities',
        store=True
    )

    total_virtual_available = fields.Float(
        string='Total Forecast Quantity',
        compute='_compute_total_quantities',
        store=True
    )

    @api.depends(
        'variant_ids.qty_available',
        'variant_ids.virtual_available'
    )
    def _compute_total_quantities(self):
        for record in self:
            record.total_qty_available = sum(
                record.variant_ids.mapped('qty_available')
            )
            record.total_virtual_available = sum(
                record.variant_ids.mapped('virtual_available')
            )

    @api.depends('variant_ids')
    def _compute_variant_count(self):
        for record in self:
            record.variant_count = len(record.variant_ids)

    def action_generate_variants(self):
        """Generate product variants based on sizes and colors"""
        self.ensure_one()

        if not self.size_ids or not self.color_ids:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Warning',
                    'message': 'Please select at least one size and one color!',
                    'type': 'warning',
                    'sticky': False,
                }
            }

        # Delete existing variants if regenerating
        self.variant_ids.unlink()

        # Create new variants
        variants_to_create = []
        for size in self.size_ids:
            for color in self.color_ids:
                variants_to_create.append({
                    'shoe_product_id': self.id,
                    'size_id': size.id,
                    'color_id': color.id,
                    'list_price': self.list_price,
                    'standard_price': self.standard_price,
                })

        # Batch create for better performance
        self.env['shoe.product.variant'].create(variants_to_create)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'{self.variant_count} variants generated successfully!',
                'type': 'success',
                'sticky': False,
            }
        }