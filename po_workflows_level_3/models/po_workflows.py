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
 
    
# class AccountInvoice(models.Model):
#     _inherit = "account.invoice"
# 
#     option = fields.Selection([('sale','B2B Sales'),
#                                ('pos','POS'),
#                                ('dis','Distributor Sale'),
#                                
#                                ],string='Sale Type')
#     
#     option2 = fields.Selection([
#                                ('wh','WareHouse'),
#                                ('ho','Head Office'),
#                                
#                                ],string='Select')
#     state = fields.Selection([
#             ('draft','Draft'),
#             ('proforma', 'Pro-forma'),
#             ('proforma2', 'Pro-forma'),
#             ('open', 'Open'),
#             
#             ('seniorac','Senior Accounts'),
#             ('hac','Head of Accounts'),
#             ('dir','Director'),
#             ('sa','Special Approval'),
#             
#             ('posseniorac','Senior Accounts'),
#             ('poshac','Head of Accounts'),
#             ('pend', 'pending'),
#             ('paid', 'Paid'),
#             ('cancel', 'Cancelled'),
#         ], string='Status', index=True, readonly=True, default='draft',
#         track_visibility='onchange', copy=False)
# 
#     special_approval = fields.Boolean("Special Approval",default=False,copy=False)
# 
#     @api.onchange('invoice_line_ids')
#     def spec_appro(self):
#         a = self.ensure_one()
# #         self.special_approval = True
#         if(self._context.get('default_invoice_id')):
#             self.update({'special_approval':True})
# #     @api.one
# #     def _get_outstanding_info_JSON(self):
# #         res = super(AccountInvoice, self)._get_outstanding_info_JSON()
# #         if self.state == 'pend':
# #             domain = [('account_id', '=', self.account_id.id), ('partner_id', '=', self.env['res.partner']._find_accounting_partner(self.partner_id).id), ('reconciled', '=', False), ('amount_residual', '!=', 0.0)]
# #             if self.type in ('out_invoice', 'in_refund'):
# #                 domain.extend([('credit', '>', 0), ('debit', '=', 0)])
# #                 type_payment = _('Outstanding credits')
# #             else:
# #                 domain.extend([('credit', '=', 0), ('debit', '>', 0)])
# #                 type_payment = _('Outstanding debits')
# #             info = {'title': '', 'outstanding': True, 'content': [], 'invoice_id': self.id}
# #             lines = self.env['account.move.line'].search(domain)
# #             currency_id = self.currency_id
# #             if len(lines) != 0:
# #                 for line in lines:
# #                     # get the outstanding residual value in invoice currency
# #                     if line.currency_id and line.currency_id == self.currency_id:
# #                         amount_to_show = abs(line.amount_residual_currency)
# #                     else:
# #                         amount_to_show = line.company_id.currency_id.with_context(date=line.date).compute(abs(line.amount_residual), self.currency_id)
# #                     if float_is_zero(amount_to_show, precision_rounding=self.currency_id.rounding):
# #                         continue
# #                     info['content'].append({
# #                         'journal_name': line.ref or line.move_id.name,
# #                         'amount': amount_to_show,
# #                         'currency': currency_id.symbol,
# #                         'id': line.id,
# #                         'position': currency_id.position,
# #                         'digits': [69, self.currency_id.decimal_places],
# #                     })
# #                 info['title'] = type_payment
# #                 self.outstanding_credits_debits_widget = json.dumps(info)
# #                 self.has_outstanding = True
# #         return res
# #     
#     @api.multi
#     def button_seniorac(self):
#         self.write({'state':'hac'})
#     
#     @api.multi
#     def reset_to_draft(self):
#         self.write({'state':'draft'})
#         
#     @api.multi
#     def button_hac(self):
# #         if (self.option=sale || option =pos):
#         
#         if(self.amount_total >50000):
#             if(self.special_approval):
#                 self.write({'state':'sa'})
#             else:
#                 self.write({'state':'dir'})
#         else:
#             if(self.special_approval):
#                 self.write({'state':'sa'})
#             else:
#                 self.action_invoice_open()
#         
#     @api.multi    
#     def button_dir(self):
#         self.action_invoice_open()
#     
#     @api.multi    
#     def button_dsa(self):
#         return self.action_invoice_open()
#     @api.multi
#     def button_posseniorac(self):
#         self.write({'state':'poshac'})
#     
#     @api.multi
#     def button_poshac(self):
#         if(self.special_approval):
#                 self.write({'state':'sa'})
#         else:
#             self.action_invoice_open()   
#         
#       
#     @api.constrains('option')
#     @api.onchange('purchase_id')
#     def purchase_order_change(self):
#         print('33')
#         
#         if not self.purchase_id:
#             return {}
#         if not self.partner_id:
#             self.partner_id = self.purchase_id.partner_id.id
#         self.option2 = self.purchase_id.option
#         print(self.purchase_id.option)
#         new_lines = self.env['account.invoice.line']
#         for line in self.purchase_id.order_line - self.invoice_line_ids.mapped('purchase_line_id'):
#             data = self._prepare_invoice_line_from_po_line(line)
#             new_line = new_lines.new(data)
#             new_line._set_additional_fields(self)
#             new_lines += new_line
#  
#         self.invoice_line_ids += new_lines
#         self.purchase_id = False
#         return {}    
#     
#     @api.multi
#     def action_invoice_open(self):
#         # lots of duplicate calls to action_invoice_open, so we remove those already open
#         view_id = self.env.ref('account.view_account_payment_invoice_form').id
#         context = dict(self.env.context or {})
#         
#         to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
#         if to_open_invoices.filtered(lambda inv: inv.state not in ['proforma2', 'draft','poshac','hac','dir','sa']):
#             raise UserError(_("Invoice must be in draft or Pro-forma state in order to validate it."))
#         to_open_invoices.action_date_assign()
#         to_open_invoices.action_move_create()
#          
#          
#          
#         return to_open_invoices.invoice_validate()  
#     
# #     @api.multi
# #     def action_invoice_paid(self):
# #         # lots of duplicate calls to action_invoice_paid, so we remove those already paid
# #         to_pay_invoices = self.filtered(lambda inv: inv.state != 'paid')
# #         if to_pay_invoices.filtered(lambda inv: inv.state != 'open'):
# #             raise UserError(_('Invoice must be validated in order to set it to register payment.'))
# #         if to_pay_invoices.filtered(lambda inv: not inv.reconciled):
# #             raise UserError(_('You cannot pay an invoice which is partially paid. You need to reconcile payment entries first.'))
# #         
# #         return to_pay_invoices.write({'state': 'pend'})
#     @api.multi
#     def action_invoice_paid2(self,s):
#         # lots of duplicate calls to action_invoice_paid, so we remove those already paid
#         to_pay_invoices = s.filtered(lambda inv: inv.state != 'pending')
# #         if to_pay_invoices.filtered(lambda inv: inv.state != 'open'):
# #             raise UserError(_('Invoice must be validated in order to set it to register payment.'))
# #         if to_pay_invoices.filtered(lambda inv: not inv.reconciled):
# #             raise UserError(_('You cannot pay an invoice which is partially paid. You need to reconcile payment entries first.'))
#         return to_pay_invoices.write({'state': 'pend'})
#     
#     
#     @api.multi
#     def action_invoice_paid1(self,s):
#         # lots of duplicate calls to action_invoice_paid, so we remove those already paid
#         to_pay_invoices = s.filtered(lambda inv: inv.state != 'paid')
# #         if to_pay_invoices.filtered(lambda inv: inv.state != 'pend'):
# #             raise UserError(_('Invoice must be validated in order to set it to register payment.'))
# #         if to_pay_invoices.filtered(lambda inv: not inv.reconciled):
# #             raise UserError(_('You cannot pay an invoice which is partially paid. You need to reconcile payment entries first.'))
#         return to_pay_invoices.write({'state': 'paid'})
# 
#     @api.multi
#     def action_invoice_draft(self):
#         if self.filtered(lambda inv: inv.state != 'cancel'):
#             raise UserError(_("Invoice must be cancelled in order to reset it to draft."))
#         # go from canceled state to draft state
#         self.write({'state': 'draft', 'date': False})
#    
#    
# # class account_line(models.Model):
# #     _inherit = "account.invoice.line"        
# #         
# #     @api.onchange('product_id','quantity')
# #     def spec_appro(self):
# #         self.ensure_one()
# # #         self.special_approval = True
# #         self.env['account.invoice'].search([('id','=',self._context['default_invoice_id'])]).update({'special_approval':True})
#     
# class Picking1(models.Model):
#     _inherit = "stock.picking"        
#         
#     optionss = fields.Selection([('sale','B2B Sales'),
#                                ('pos','POS'),
#                                ('wh','WareHouse'),
#                                ('ho','Head Office'),
#                                ('dis','Distributor Sale'),
#                                
#                                
#                                ],required=True,string='Sale Type')   
#     
#     purchase_id = fields.Many2one('purchase.order', related='move_lines.purchase_line_id.order_id',
#         string="Purchase Orders", readonly=True)
#     sale_id = fields.Many2one('sale.order', "Sale Order")
#     
#     grn = fields.Char("Party's GRN No")
#     
#     sale_ids = fields.Char(related='sale_id.name')
#     purchase_ids = fields.Char(related='purchase_id.name') 
#     state = fields.Selection([
#         ('draft', 'Draft'), ('cancel', 'Cancelled'),
#         ('waiting', 'Waiting Another Operation'),
#         ('confirmed', 'Waiting Availability'),
#         ('partially_available', 'Partially Available'),
#          ('acc','Accountant'),
#         ('sic','Store In-charge'),
#         ('assigned', 'Available'), 
#         
#         ('seniorac','Senior Accounts'),
#         ('pma','Production manager/Accountant'),
#         ('dir','Director'),
#         ('hac','Head of Accounts'),
#         ('damt','Director'),
#        
#         ('done', 'Done')], string='Status', compute='_compute_state',
#         copy=False, index=True, readonly=True, store=True, track_visibility='onchange',)
#     
#     
#     
#     def acc(self):
# #         self.write({'state':'sic'})
#         return self.do_new_transfer()
#     
#     def sic(self):
#         self.write({'state':'acc'})
#         
#         
#         
#     @api.multi
#     def button_seniorac(self):
#         self.write({'state':'hac'})
#     
#     @api.multi
#     def button_hac(self):
#         
#         self.write({'state':'damt'})
#         
#         
#     @api.multi    
#     def button_damt(self):
#         return self.do_new_transfer()
#         
#         
#     @api.multi
#     def button_pma(self):
#         
#         self.write({'state':'dir'})
#         
#         
# class MrpProduction(models.Model):
#     
#     _inherit = 'mrp.production'
#      
#     state = fields.Selection([
#         ('sac','Senior Accounts'),
#         ('dir','Director'),
#         ('draft','Draft'),
#         ('confirmed', 'Confirmed'),
#         ('planned', 'Planned'),
#         ('progress', 'In Progress'),
#         ('done', 'Done'),
#         ('cancel', 'Cancelled')], string='State',
#         copy=False, default='confirmed', track_visibility='onchange')
#     
#     
#     def sac(self):
#         self.write({'state':'dir'})
#         
#     def dir(self):
#         self.write({'state':'draft'})
#         
#     @api.multi
#     def button_plan(self):
#         """ Create work orders. And probably do stuff, like things. """
#         orders_to_plan = self.filtered(lambda order: order.routing_id and order.state == 'draft')
#         for order in orders_to_plan:
#             quantity = order.product_uom_id._compute_quantity(order.product_qty, order.bom_id.product_uom_id) / order.bom_id.product_qty
#             boms, lines = order.bom_id.explode(order.product_id, quantity, picking_type=order.bom_id.picking_type_id)
#             order._generate_workorders(boms)
#         return orders_to_plan.write({'state': 'planned'})
#     
# 
# class MrpWorkorder(models.Model):
#     _inherit = 'mrp.workorder'
#     
#     
#     state = fields.Selection([
#         ('sac','Senior Accounts'),
#         ('dir','Director'),
#         ('done1','Confirm'),
#         ('pending', 'Pending'),
#         ('ready', 'Ready'),
#         ('progress', 'In Progress'),
#         ('done', 'Finished'),
#         ('cancel', 'Cancelled')], string='Status',
#         default='pending')
#     
#     def sac(self):
#         self.write({'state':'dir'})
#         
#     def dir(self):
#         self.write({'state':'done1'})
#         
# 
# class ProductTemp(models.Model):
#     _inherit = "product.template" 
#     
#     state = fields.Selection([
#         
#         ('accstore', 'Accountant/ Store In-charge'),
#         ('dir', 'Directors'),
#         ('done', 'Done'),
#         ], string='Status',
#         default='accstore')
#     
#     def accstore(self):
#         self.write({'state':'dir'})
#         
#     def reset(self):
#         self.write({'state':'dir'})
#     def dir(self):
#         self.write({'state':'done'})
#     
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(ProductTemp, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
#         if view_type=="form":
#             doc = etree.XML(result['arch'])
#             for node in doc.iter(tag="field"):
#                 if 'readonly' in node.attrib.get("modifiers",''):
#                     attrs = node.attrib.get("attrs",'')
#                     if 'readonly' in attrs:
#                         attrs_dict = safe_eval(node.get('attrs'))
#                         r_list = attrs_dict.get('readonly',)
#                         if type(r_list)==list:
#                             r_list.insert(0,('state','=','done'))
#                             if len(r_list)>1:
#                                 r_list.insert(0,'|')
#                         attrs_dict.update({'readonly':r_list})
#                         node.set('attrs', str(attrs_dict))
#                         setup_modifiers(node, result['fields'][node.get("name")])
#                         continue
#                     else:
#                         continue
#                 node.set('attrs', "{'readonly':[('state','=','done')]}")
#                 setup_modifiers(node, result['fields'][node.get("name")])
#                  
#             result['arch'] = etree.tostring(doc)
#         return result
#     
#     
#     @api.model
#     def name_search(self, name='', args=None, operator='ilike', limit=1000000):
#         if not args:
#             args = []
#         args += [['state','=','done']]
#         res = super(ProductTemp,self).name_search(name, args, operator, limit)
#         return  res
#     
#     
# class ProductProduct(models.Model):
#     _inherit = "product.product" 
#     
#     state = fields.Selection([
#         
#         ('accstore', 'Accountant/ Store In-charge'),
#         ('dir', 'Directors'),
#         ('done', 'Done'),
#         ], string='Status',
#         default='accstore')
#     
#     def accstore(self):
#         self.write({'state':'dir'})
#         
#     def reset(self):
#         self.write({'state':'dir'})
#     def dir(self):
#         self.write({'state':'done'})
#     
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(ProductProduct, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
#         if view_type=="form":
#             doc = etree.XML(result['arch'])
#             for node in doc.iter(tag="field"):
#                 if 'readonly' in node.attrib.get("modifiers",''):
#                     attrs = node.attrib.get("attrs",'')
#                     if 'readonly' in attrs:
#                         attrs_dict = safe_eval(node.get('attrs'))
#                         r_list = attrs_dict.get('readonly',)
#                         if type(r_list)==list:
#                             r_list.insert(0,('state','=','done'))
#                             if len(r_list)>1:
#                                 r_list.insert(0,'|')
#                         attrs_dict.update({'readonly':r_list})
#                         node.set('attrs', str(attrs_dict))
#                         setup_modifiers(node, result['fields'][node.get("name")])
#                         continue
#                     else:
#                         continue
#                 node.set('attrs', "{'readonly':[('state','=','done')]}")
#                 setup_modifiers(node, result['fields'][node.get("name")])
#                  
#             result['arch'] = etree.tostring(doc)
#         return result
# 
#     @api.model
#     def name_search(self, name='', args=None, operator='ilike', limit=1000000):
#         if not args:
#             args = []
#         args += [['state','=','done']]
#         res = super(ProductProduct,self).name_search(name, args, operator, limit)
#         return  res 
#  
#     
# class StockMove(models.Model):
#     _inherit = "stock.move"
#     
#     def _get_new_picking_values(self):
#         """ Prepares a new picking for this move as it could not be assigned to
#         another picking. This method is designed to be inherited. """
#         return {
#             'origin': self.origin,
#             'company_id': self.company_id.id,
#             'move_type': self.group_id and self.group_id.move_type or 'direct',
#             'partner_id': self.partner_id.id,
#             'picking_type_id': self.picking_type_id.id,
#             'location_id': self.location_id.id,
#             'location_dest_id': self.location_dest_id.id,
#             'optionss':self.procurement_id.sale_line_id.order_id.optionss
#         }
#         
#         
#     @api.multi
#     def assign_picking(self):
#         result = super(StockMove, self).assign_picking()
#         for move in self:
#             if move.picking_id and move.picking_id.group_id:
#                 picking = move.picking_id
#                 order = self.env['sale.order'].sudo().search([('procurement_group_id', '=', picking.group_id.id)])
#                 picking.message_post_with_view(
#                     'mail.message_origin_link',
#                     values={'self': picking, 'origin': order,'optionss':order.optionss},
#                     subtype_id=self.env.ref('mail.mt_note').id)
#         return result    
# 
# 
# 
# class Inventory(models.Model):
#     _inherit = "stock.inventory"
#     
#     state = fields.Selection(string='Status', selection=[
#         ('draft', 'Draft'),
#         ('cancel', 'Cancelled'),
#         ('confirm', 'In Progress'),
#         ('pmas','Production Manager/ Sore In-charge'),
#         ('hoa_dir','Head of Accounts/directors'),
#         ('done', 'Validated')],
#         copy=False, index=True, readonly=True,
#         default='draft')
#     
#     def button_pmas(self):
#         self.write({'state':'hoa_dir'})
#         
# # class Sale(models.Model):
# #    _inherit = "sale.order"
#    
#    
#    
#    
#         
#         
# class Partner(models.Model):
#     _inherit = "res.partner"
#     
#     cla_approval1 = fields.Boolean("Credit Limit Approval",default=False, copy=False)
#     reset1 = fields.Boolean("Reset" ,default=False)
#     special_approval = fields.Boolean("Price Limit Approval",default=False, copy=False)
#      
#     state = fields.Selection([
#         ('sac','Senior Accounts'),
#         ('hoa','Head of Accounts'),
#         ('vsac','Senior Accounts'),
#         ('dsa','Price List Approval'),
#         ('cre','Credit Limit Approval'),
#         ('vhoa','Head of Accounts/directors'),
#         ('done','Done'),
#         ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='sac')
#     
#     
#     
#             
#     @api.onchange('property_product_pricelist')
#     def spec_appro(self):
#         
#         a = self.ensure_one()
#         if(self.property_product_pricelist):
#             self.update({'special_approval':True})
#         
#         
#     @api.onchange('credit_limit')
#     def cla_appro(self):
#         
#         a = self.ensure_one()
#         if(self.reset1):
#             if(self.credit_limit):
#                 self.update({'cla_approval1':True})
#                 
#                 
#     def button_sac(self):
#         self.write({'state':'hoa'})
#     
#     def button_dsa(self):
#         self.write({'state':'done'})
#     
#     def button_cre(self):
#         self.write({'state':'done'})
#     
#     def reset2(self):
#         self.update({'special_approval' : False})
#         self.update({'cla_approval1' : False}) 
#         self.update({'reset1':True})
#         self.write({'state':'sac'})
# 
# 
#     def button_hoa(self):
#         if(self.special_approval and self.cla_approval1):
#             self.write({'state':'dsa'})
#         else:
#             if(self.cla_approval1):
#                 self.write({'state':'cre'})
#             else:
#                 if(self.special_approval):
#                     self.write({'state':'dsa'})
#                 else:    
#                     self.write({'state':'done'})
#     
#     def button_ven_sac(self):
#         self.write({'state':'done'})
#     
#     def button_ven_hoa(self):
#         if(self.special_approval) and (self.cla_approval1):
#             self.write({'state':'dsa'})
#         else:
#             if(self.cla_approval1):
#                 self.write({'state':'cre'})
#             else:
#                 if(self.special_approval):
#                     self.write({'state':'dsa'})
#                 else:    
#                     self.write({'state':'done'})
# #     
# #         if(self.cla_approval1):
# #             self.write({'state':'dsa'})
# #         else:
# #             self.write({'state':'done'})
# #     
#     @api.model
#     def name_search(self, name='', args=None, operator='ilike', limit=1000000):
#         if not args:
#             args = []
#         args += [['state','=','done']]
#         res = super(Partner,self).name_search(name, args, operator, limit)
#         return  res
#     
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(Partner, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
#         if view_type=="form":
#             doc = etree.XML(result['arch'])
#             for node in doc.iter(tag="field"):
#                 if 'readonly' in node.attrib.get("modifiers",''):
#                     attrs = node.attrib.get("attrs",'')
#                     if 'readonly' in attrs:
#                         attrs_dict = safe_eval(node.get('attrs'))
#                         r_list = attrs_dict.get('readonly',)
#                         if type(r_list)==list:
#                             r_list.insert(0,('state','=','done'))
#                             if len(r_list)>1:
#                                 r_list.insert(0,'|')
#                         attrs_dict.update({'readonly':r_list})
#                         node.set('attrs', str(attrs_dict))
#                         setup_modifiers(node, result['fields'][node.get("name")])
#                         continue
#                     else:
#                         continue
#                 node.set('attrs', "{'readonly':[('state','=','done')]}")
#                 setup_modifiers(node, result['fields'][node.get("name")])
#                  
#             result['arch'] = etree.tostring(doc)
#         return result
#     
#     def reset(self):
#         self.write({'state':'sac'})
# class AccountMove(models.Model):
#     _inherit = "account.move"
#     
#     cheque = fields.Char('Cheque No.')
#     
#     state = fields.Selection([
#                             
#                             
#                             ('draft','Senior Accounts'),
#                             ('hac','Head of Accounts'),
#                             ('dir','Director'),
#                             ('sa','Special Approval'),
#                               
#                             ('posted', 'Posted')
#                             
#                             
#                             ], string='Status',
#       required=True, readonly=True, copy=False, default='draft')
#     
#     @api.multi
#     def button_seniorac(self):
#         self.write({'state':'hac'})
#     
#     @api.multi
#     def button_hac(self):
#         if(self.amount >50000):
#             self.write({'state':'dir'})
#         else:
#             return self.post()
#     
#  
#     def button_dir(self):
#         return self.post()
#     
# class AccountPayment(models.Model):
#     _inherit = "account.payment"
#     
#     option = fields.Selection([('sale','B2B Sales'),
#                                ('pos','POS'),
#                                ('dis','Distributor Sale'),
#                                
#                                ],string='Sale Type')
#     
#     
#     state = fields.Selection([('draft','Senior Accounts'),
#                               ('hac','Head of Accounts'),
#                               ('dir','Director'),
#                               ('sa','Special Approval'),
#                               ('posted', 'Posted'), 
#                               ('sent', 'Sent'), 
#                               ('reconciled', 'Reconciled')], readonly=True, default='draft', copy=False, string="Status")
#     
#     cheque = fields.Char('Cheque No.')
#     difference = fields.Char('Payment Difference',readonly='true')
#     other_bank = fields.Char('Adjusted Account',readonly='true')
#     
#      
#     @api.multi
#     def unlink(self):
#         for leave in self:
#             if leave.state in ('draft','hac','sa'):
#                 raise UserError(_('You cannot delete any Payment form. '))
#                   
# 
#     
#     @api.multi
#     def button_seniorac(self):
#         self.write({'state':'hac'})
#     
#     @api.multi
#     def button_hac(self):
#         if(self.payment_type == "outbound"):
#             if(self.amount > 50000):
#                 self.write({'state':'dir'})
#             else:
#                 self.post_by_hac()
#         else:
#             if(self.amount > 50000):
#                 if(self.payment_difference_handling == 'open'):
#                     self.write({'state':'dir'})
#             
#                 else:
#                     if(self.payment_difference_handling == 'reconcile'):
#                         self.write({'state':'sa'})
#             else:
#                 if(self.payment_difference_handling == 'reconcile'):
#                     self.write({'state':'sa'})
#                 else:        
#                     self.post_by_hac()
#              
#                 
#     @api.multi    
#     def button_dsa(self):
#         return self.post_by_hac()
#     
#     @api.multi
#     def reset_to_draft(self):
#         self.write({'state':'draft'})
#       
#     
#     def _get_move_vals(self, journal=None):
#         """ Return dict to create the payment move
#         """
#         journal = journal or self.journal_id
#         if not journal.sequence_id:
#             raise UserError(_('Configuration Error !'), _('The journal %s does not have a sequence, please specify one.') % journal.name)
#         if not journal.sequence_id.active:
#             raise UserError(_('Configuration Error !'), _('The sequence of journal %s is deactivated.') % journal.name)
#         name = self.move_name or journal.with_context(ir_sequence_date=self.payment_date).sequence_id.next_by_id()
#         return {
#             'name': name,
#             'date': self.payment_date,
#             'ref': self.communication or '',
#             'company_id': self.company_id.id,
#             'journal_id': journal.id,
#             'payment_type': self.payment_type,
#             'cheque':self.cheque
#         }
#     
#     
#     
#     @api.multi
#     def post_by_hac(self):
#         """ Create the journal items for the payment and update the payment's state to 'posted'.
#             A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
#             and another in the destination reconciliable account (see _compute_destination_account_id).
#             If invoice_ids is not empty, there will be one reconciliable move line per invoice to reconcile with.
#             If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
#         """
#         for rec in self:
# 
#             if rec.state not in ['draft','hac','dir','sa']:
#                 raise UserError(_("Only a draft payment can be posted. Trying to post a payment in state %s.") % rec.state)
# 
#             if any(inv.state != 'pend' for inv in rec.invoice_ids):
#                 raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))
# 
#             # Use the right sequence to set the name
#             if rec.payment_type == 'transfer':
#                 sequence_code = 'account.payment.transfer'
#             else:
#                 if rec.partner_type == 'customer':
#                     if rec.payment_type == 'inbound':
#                         sequence_code = 'account.payment.customer.invoice'
#                     if rec.payment_type == 'outbound':
#                         sequence_code = 'account.payment.customer.refund'
#                 if rec.partner_type == 'supplier':
#                     if rec.payment_type == 'inbound':
#                         sequence_code = 'account.payment.supplier.refund'
#                     if rec.payment_type == 'outbound':
#                         sequence_code = 'account.payment.supplier.invoice'
#             rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
# 
#             # Create the journal entry
#             amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
#             if self.move_name == False:
#                 move = rec._create_payment_entry(amount)
# 
#             # In case of a transfer, the first journal entry created debited the source liquidity account and credited
#             # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
#                 if rec.payment_type == 'transfer':
#                     transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
#                     transfer_debit_aml = rec._create_transfer_entry(amount)
#                     (transfer_credit_aml + transfer_debit_aml).reconcile()
# 
#             rec.write({'state': 'posted', 'move_name': self.move_name})   
#             inv1 = self.env['account.invoice']
#             inv1.action_invoice_paid1(self.invoice_ids)
#     
#     @api.multi
#     def post(self):
#         """ Create the journal items for the payment and update the payment's state to 'posted'.
#             A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
#             and another in the destination reconciliable account (see _compute_destination_account_id).
#             If invoice_ids is not empty, there will be one reconciliable move line per invoice to reconcile with.
#             If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
#         """
#         for rec in self:
# 
#             if rec.state not in ['draft','hac','dir','sa']:
#                 raise UserError(_("Only a draft payment can be posted. Trying to post a payment in state %s.") % rec.state)
# 
#             if any(inv.state != 'open' for inv in rec.invoice_ids):
#                 raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))
# 
#             # Use the right sequence to set the name
#             if rec.payment_type == 'transfer':
#                 sequence_code = 'account.payment.transfer'
#             else:
#                 if rec.partner_type == 'customer':
#                     if rec.payment_type == 'inbound':
#                         sequence_code = 'account.payment.customer.invoice'
#                     if rec.payment_type == 'outbound':
#                         sequence_code = 'account.payment.customer.refund'
#                 if rec.partner_type == 'supplier':
#                     if rec.payment_type == 'inbound':
#                         sequence_code = 'account.payment.supplier.refund'
#                     if rec.payment_type == 'outbound':
#                         sequence_code = 'account.payment.supplier.invoice'
#             rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
# 
#             # Create the journal entry
#             amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
#             rec.update({'difference':self.payment_difference,'other_bank':self.writeoff_account_id.name,'option':self.invoice_ids.option})
#            
#             
#             inv1 = self.env['account.invoice']
#             inv1.action_invoice_paid2(self.invoice_ids)
#             # In case of a transfer, the first journal entry created debited the source liquidity account and credited
#             # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
#             
# 
#             rec.write({'state': 'draft'})
#             
# # class account_register_payments1(models.TransientModel):
# #     
# #     _inherit = 'account.abstract.payment'
# #     
# #     def get_payment_vals(self):
# #         """ Hook for extension """
# #         return {
# #             'journal_id': self.journal_id.id,
# #             'payment_method_id': self.payment_method_id.id,
# #             'payment_date': self.payment_date,
# #             'communication': self.communication,
# #             'invoice_ids': [(4, inv.id, None) for inv in self._get_invoices()],
# #             'payment_type': self.payment_type,
# #             'amount': self.amount,
# #             'currency_id': self.currency_id.id,
# #             'partner_id': self.partner_id.id,
# #             'partner_type': self.partner_type,
# #         }
# #             
# 
# 
# 
# 
# class ProductPricelist(models.Model):
#     _inherit = 'product.pricelist'
#  
#     state = fields.Selection([
#                             
#                                 ('dir','Director'),
#                                 ('done','Done'),
#                                 
#                             ], string='Status', readonly=True, default='dir', copy=False,)
# 
#     
#     
#     def reset(self):
#         
#         self.write({'state':'dir'})    
#  
#     
#         
#     @api.multi
#     def button_dir(self):
#         
#         self.write({'state': 'done'})
#         
#     
#     @api.model
#     def name_search(self, name='', args=None, operator='ilike', limit=5000000):
#         if not args:
#             args = []
#         args += [['state','=','done']]
#         res = super(ProductPricelist,self).name_search(name, args, operator, limit)
#         return  res    
#         
#         