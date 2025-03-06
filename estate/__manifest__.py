{
    'name': "Estate",
    'depends': ['base'],
    'data': [
        'data/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offer_views.xml',

        'views/estate_menu_views.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}