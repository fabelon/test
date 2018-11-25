import time
from odoo import models, api
# from reportlab.lib._rl_accel import Penalty
from datetime import datetime
import calendar
# from . import tenancy_rent_schedule


class tenant_payment(models.Model):
    _name = 'report.pragmatic_property_extension.report_tenant_payment'

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(
            self.env.context.get('active_ids', []))
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data,
            'docs': docs,
            'time': time,
            'get_details': self.get_details,
        }
        return self.env['report'].render('pragmatic_property_extension.report_tenant_payment', docargs)

    def get_details(self, start_date, end_date):
        payment_obj = self.env["account.payment"]
        payment_ids = payment_obj.search([('payment_date', '>=', start_date), ('payment_date', '<=', end_date)]).ids
        return payment_obj.browse(payment_ids)
    
#     
  
            
        
         
        
         
#         
    class account_analytic_account(models.Model):
         
        _inherit= 'account.analytic.account'
         
        Total = 0.0
        
        def fetch_late_fees(self):
            rent_schedule_ids =[]
            rent_schedule_ids  =self.env['tenancy.rent.schedule'].search([('tenancy_id','=',self.id),('rel_tenant_id','=',self.tenant_id.id)])
            penalty1 = 0.0
            currentMonth = datetime.now().month
            currentyear = datetime.now().year
            for rent_scedule_id in rent_schedule_ids:
                month = datetime.strptime(rent_scedule_id.rent_from_date, '%Y-%m-%d').strftime('%m')
                year = datetime.strptime(rent_scedule_id.rent_from_date, '%Y-%m-%d').strftime('%Y')
                if (int(month) == currentMonth-1 or int(month) == currentMonth-2 and int(year) == currentyear and not rent_scedule_id.paid):
                    penalty1 = penalty1 + rent_scedule_id.penalty_amount
            return penalty1
        
        def previous_outstanding(self):  
            rent_schedule_ids  =self.env['tenancy.rent.schedule'].search([('tenancy_id','=',self.id),('rel_tenant_id','=',self.tenant_id.id)])
            pend_bal = 0.0
            currentMonth = datetime.now().month
            currentyear = datetime.now().year
            for rent_scedule_id in rent_schedule_ids:
                month = datetime.strptime(rent_scedule_id.rent_from_date, '%Y-%m-%d').strftime('%m')
                year = datetime.strptime(rent_scedule_id.rent_from_date, '%Y-%m-%d').strftime('%Y')
                if (int(month) == currentMonth-2 and int(year) == currentyear and not rent_scedule_id.paid):
                    print (' the Month is =====', month,year)
                    pend_bal =pend_bal+((rent_scedule_id.amount)-rent_scedule_id.amount_already_paid) 
            return pend_bal
        
        def fetch_total_balance(self):
            rent_schedule_ids  =self.env['tenancy.rent.schedule'].search([('tenancy_id','=',self.id),('rel_tenant_id','=',self.tenant_id.id)])
            bal = 0.0
            security_deposit = self.deposit
            sd = self.deposit
            maint_amount= 0.0
            currentMonth = datetime.now().month
            currentyear = datetime.now().year
            for rent_scedule_id in rent_schedule_ids:
                month = datetime.strptime(rent_scedule_id.rent_from_date, '%Y-%m-%d').strftime('%m')
                year = datetime.strptime(rent_scedule_id.rent_from_date, '%Y-%m-%d').strftime('%Y')
                if (int(month)==currentMonth-1 or int(month)==currentMonth-2 and int(year) == currentyear and not rent_scedule_id.paid):
                    bal = bal +((rent_scedule_id.amount + rent_scedule_id.penalty_amount))-rent_scedule_id.amount_already_paid
                    maint_amount = self.invoices_from_mantanance()
                    print ('maintanace_amount =====', maint_amount,bal,sd)
                    sd = sd - (bal + maint_amount)
#                     sd += rent_scedule_id.amount_already_paid
            return sd
            
        def invoices_from_mantanance(self): 
            mantainace_id = []
            currentMonth = datetime.now().month
            currentyear = datetime.now().year
            mantaince_id  =self.env['property.maintenance'].search([('property_id','=',self.property_id.id),('tenant_id','=',self.tenant_id.id)])
            tot = 0.0
            for maintance_line in mantaince_id:
                month = datetime.strptime(maintance_line.date, '%Y-%m-%d').strftime('%m')
                year = datetime.strptime(maintance_line.date, '%Y-%m-%d').strftime('%Y')
                if (int(month) == currentMonth or int(month) == currentMonth-1 and int(year) == currentyear):
                    tot  += maintance_line.amount_total         
            return tot
        
        def fetch_rent(self):
            rent_schedule_ids  =self.env['tenancy.rent.schedule'].search([('tenancy_id','=',self.id),('rel_tenant_id','=',self.tenant_id.id)])
            currentMonth = datetime.now().month
            currentyear = datetime.now().year
            rent= 0.00
            for rent_scedule_id in rent_schedule_ids:
                month = datetime.strptime(rent_scedule_id.rent_from_date, '%Y-%m-%d').strftime('%m')
                year = datetime.strptime(rent_scedule_id.rent_from_date, '%Y-%m-%d').strftime('%Y')
                if (int(month) == currentMonth-1 and int(year) == currentyear):
                    rent = rent_scedule_id.amount - rent_scedule_id.amount_already_paid
                    print (' the Month is =====', month,year)
                   
            return rent
#           
            
            
    class tenant_details(models.Model):
         
        _inherit= 'tenant.partner'
        
        @api.one
        def get_current_month(self):
            
            currentMonth = datetime.now().month
            fetch_month=calendar.month_name[currentMonth]
            return fetch_month
        
        @api.one
        def get_current_year(self):
            currentyear = datetime.now().year
            return currentyear
            
        @api.one
        def fetch_total_rent(self):
            rent_schedule_ids =[]
            bal,maint_amount,tot = 0.00,0.00,0.00
            account_ids  =self.env['account.analytic.account'].search([('tenant_id','=',self.id)])
            
            currentyear = datetime.now().year
            currentMonth = datetime.now().month
            rent_schedule_ids =[]
           
            for account_id in account_ids:
                sd = account_id.deposit
                rent_schedule_ids  =self.env['tenancy.rent.schedule'].search([('rel_tenant_id','=',account_id.tenant_id.id),('property_id','=',account_id.property_id.id)])
                for rent_scedule_id in rent_schedule_ids:
                    mantaince_id  =self.env['property.maintenance'].search([('property_id','=',rent_scedule_id.property_id.id),('tenant_id','=',rent_scedule_id.rel_tenant_id.id)])
                    month = datetime.strptime(rent_scedule_id.rent_from_date, '%Y-%m-%d').strftime('%m')
                    year = datetime.strptime(rent_scedule_id.rent_from_date, '%Y-%m-%d').strftime('%Y')
                    if ( int(month)==currentMonth-1 or int(month) == currentMonth-2 and int(year) == currentyear and not rent_scedule_id.paid ):
                        tot = 0.0
                        for maintance_line in mantaince_id:
                            month = datetime.strptime(maintance_line.date, '%Y-%m-%d').strftime('%m')
                            year = datetime.strptime(maintance_line.date, '%Y-%m-%d').strftime('%Y')
                            if (int(month) == currentMonth or int(month) == currentMonth-1 and int(year) == currentyear):
                                tot  += maintance_line.amount_total      
                           
                        bal = bal +((rent_scedule_id.amount + rent_scedule_id.penalty_amount)-rent_scedule_id.amount_already_paid)
                        maint_amount = tot
                        print ('maintanace_amount =====', maint_amount,bal,sd)
                        sd = sd - (bal + maint_amount)
            print ('\n\n\nsdddddddddddddddddddddddddddddddd',sd,type(sd))              
            return sd
        
       