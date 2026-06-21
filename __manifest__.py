{
    'name': 'Shoe Store Management',
    'version': '17.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Manage shoe store products with sizes and colors',
    'description': """
        Custom module for shoe store management
        - Manage shoe sizes and colors
        - Auto-generate product variants
        - Track inventory by size and color
        - POS Integration
        - Sales Reports
    """,
    'author': 'Eslam Ahmed',
    'website': 'https://yourwebsite.com',
    'depends': [
        'base',
        'product',
        'stock',
        'sale_management',
        'purchase',
        'point_of_sale',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/shoe_sizes_data.xml',
        'views/shoe_size_views.xml',
        'views/shoe_color_views.xml',
        'views/shoe_product_views.xml',
        'views/sale_order_views.xml',
        'views/menu_views.xml',
        'report/shoe_sales_report_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}