{
    'name':"App One",
    'author':"Mohamed",
    'version':'1.3',
    'category':'Education',
    'depends':[ 'base',
                'mail',
                'sale_management',
                ],

    'data':[ 'security/ir.model.access.csv',
             'security/security.xml',
             'data/sequence.xml',
            'views/base_menu.xml',
             'views/property_view.xml',
            'views/property_history.xml',
            'views/owner_view.xml',
            'views/tag.xml',
            'views/sales_order.xml',
             'views/sale_order_button_action.xml',
            'wizard/change_state_wizard_view.xml',
            'reports/university_report.xml'

          ],
    'assets': {
        'web.assets_backend': ['app_one/static/src/css/property.css',],
        'web.report.assets_common': ['app_one/static/src/css/fonts_report.css',],
    },

    'application':True ,
}
