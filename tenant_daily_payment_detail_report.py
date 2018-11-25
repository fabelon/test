from odoo import models, fields, api

class tenant_daily_payment(models.TransientModel):

    _name = 'tenant.daily.payment'

    start_date = fields.Date('Start date', required=True)
    end_date = fields.Date('End date', required=True)
    
    @api.multi
    def print_report(self):
        if self._context is None:
            self._context = {}
        data = {
            'ids': self.ids,
            'model': 'account.payment',
            'form': self.read(['start_date', 'end_date'])[0]
        }
        return self.env['report'].get_action(self, 'pragmatic_property_extension.report_tenant_payment',
                                             data=data)


