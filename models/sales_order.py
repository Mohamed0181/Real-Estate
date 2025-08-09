from odoo import models, fields

class SalesOrder(models.Model):
    _inherit = 'sale.order'  # ✅ تأكد من استخدام الاسم الصحيح للنموذج
    property_id = fields.Many2one('property')


    def action_confirm(self):
        res = super().action_confirm()  # ✅ إزالة 'sales_order' من super()
        print("Inside action confirm")  # ✅ رسالة للتأكد من تنفيذ الوظيفة
        return res



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def button_action(self):
        print("inside button action")