from odoo import models,fields
class PropertyHistory(models.Model):
    _name='property_history'
    _description = 'Property History'

    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('property')
    old_state = fields.Char()
    new_state = fields.Char()
    reason = fields.Char()
    lines_ids = fields.One2many('property_history_lines','history_id')





class PropertyHistoryLines(models.Model):
    _name = 'property_history_lines'

    history_id = fields.Many2one('property_history')
    description = fields.Char()
    area = fields.Float()
