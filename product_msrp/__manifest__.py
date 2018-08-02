{
    'name': "Product MSRP",
    'summary': """Shows the msrp and margin between sales price and msrp cost""",
    'author': 'Vayam-LLC , Ali Amer',
    'website': 'http://www.vayam-llc.com/',
    'category': 'Product',
    'version': '10.0',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'base',
        'sale',
        'purchase',
        'mclane_customization'
    ],
    'data': [
        'views/product_view_msrp.xml',
        'views/res_partner_view.xml',
        'data/ir_cron.xml',
    ],
}
