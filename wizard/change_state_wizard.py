from odoo import models , fields

class ChangeStateWizard(models.TransientModel):
    _name = 'change_state'



    property_id = fields.Many2one('property')
    state = fields.Selection([('draft','Draft'),
                              ('pending','Pending'),
    ],default='draft')
    reason = fields.Char()

    def action_confirm(self):
        if  self.property_id.state == 'close' :
           self.property_id.state = self.state
           self.property_id.create_history('close',self.state,self.reason)


