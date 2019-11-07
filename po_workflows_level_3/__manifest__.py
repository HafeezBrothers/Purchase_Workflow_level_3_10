{

    'name':'Purchase Order WorkFlows (Level 3)',
    'description' : 'PO WorkFlows',
    'author' : 'Hafeez Brothers',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends' : [
                   'base','purchase',
                ],
    'data' :[   
                
                'views/purchase_cus.xml',
                'security/hr_user_rights1.xml'
            ],
    'installable' : True,
    'price':50.00,
    'currency':'EUR', 
    

}
