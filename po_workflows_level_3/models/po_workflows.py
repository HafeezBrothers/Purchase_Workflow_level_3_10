from odoo import api, fields, models



_STATES = [
    ('draft', 'Draft'),
    ('to_approve', 'To Approve'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('done', 'Done')
]

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"   
     
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('approval1','Approve'),
        ('approval2','2nd Approval'),
        ('approval','Final Approval'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
        ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
     
   
    def btn_app1(self):
        self.write({'state':'approval2'})
    
    def btn_app2(self):
        self.write({'state':'approval'})
     
    @api.multi
    def approv1(self):
        self.button_confirm()
         
    @api.multi
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft','approval', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.user.company_id.currency_id.compute(order.company_id.po_double_validation_amount, order.currency_id))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
#                 order.write({'state2': 'to approve'})
        return True   
 
    
