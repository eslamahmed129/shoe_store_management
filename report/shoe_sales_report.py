from odoo import models, fields, tools


class ShoeSalesReport(models.Model):
    _name = 'shoe.sales.report'
    _description = 'Shoe Sales Analysis'
    _auto = False
    _rec_name = 'shoe_product_id'

    shoe_product_id = fields.Many2one('shoe.product', string='Shoe Product', readonly=True)
    size_id = fields.Many2one('shoe.size', string='Size', readonly=True)
    color_id = fields.Many2one('shoe.color', string='Color', readonly=True)
    product_id = fields.Many2one('product.product', string='Product Variant', readonly=True)
    qty_sold = fields.Float(string='Quantity Sold', readonly=True)
    revenue = fields.Float(string='Revenue', readonly=True)
    cost = fields.Float(string='Cost', readonly=True)
    profit = fields.Float(string='Profit', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY so.date_order, sol.id) as id,
                    spv.shoe_product_id,
                    spv.size_id,
                    spv.color_id,
                    sol.product_id,
                    SUM(sol.product_uom_qty) as qty_sold,
                    SUM(sol.price_subtotal) as revenue,
                    SUM(sol.product_uom_qty * COALESCE(spv.standard_price, 0)) as cost,
                    SUM(sol.price_subtotal - (sol.product_uom_qty * COALESCE(spv.standard_price, 0))) as profit,
                    so.date_order::date as date,
                    so.partner_id
                FROM sale_order_line sol
                JOIN sale_order so ON sol.order_id = so.id
                LEFT JOIN shoe_product_variant spv ON sol.product_id = spv.product_id
                WHERE so.state in ('sale', 'done')
                    AND spv.id IS NOT NULL
                GROUP BY 
                    spv.shoe_product_id,
                    spv.size_id,
                    spv.color_id,
                    sol.product_id,
                    so.date_order,
                    so.partner_id,
                    sol.id
            )
        """ % self._table)