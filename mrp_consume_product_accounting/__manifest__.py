# Copyright 2019 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

{
    'name': "WIP with consumables",
    'summary': """
            Changing the consumable product accounting for the MRP and avoid adding
            consumed product raw material cost for the finished product".
        """,
    'version': "15.0.1.0.0",
    'category': 'Uncategorized',
    'website': "http://sodexis.com/",
    'author': "Sodexis",
    'license': 'OPL-1',
    'installable': False,
    'application': False,
    'depends': [
        'account',
        'stock_account',
        'mrp_account',
    ],
    'data': [
    ],
}
