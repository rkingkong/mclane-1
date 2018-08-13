{
    'name': "Picking Hazardous",
    'summary': """Print Hazardous Documents At Delivery Slip""",
    'author': 'Vayam-LLC , Ali Amer',
    'website': 'http://www.vayam-llc.com/',
    'category': 'Product',
    'version': '10.0',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'base',
        'stock',

    ],
    'data': [
        'views/product_hazardous.xml',
        'report/delivery_report.xml',
        'security/ir.model.access.csv',


    ],
}
