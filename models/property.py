from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    active = fields.Boolean(default=1)

    name = fields.Char(required=1, default='Name', size=25, tracking=1,translate=1)
    description = fields.Text(tracking=1)
    selling_price = fields.Integer()
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    garage = fields.Boolean()
    expected_price = fields.Float()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('close', 'Closed'),
    ], default='draft')

    diff = fields.Float(compute='_compute_diff', readonly=1)
    owner_id = fields.Many2one('owner')
    owner_phone = fields.Char(related='owner_id.phone', readonly=0)
    owner_address = fields.Char(related='owner_id.address')
    tag_ids = fields.Many2many('tag')
    line_ids = fields.One2many('property.lines', 'property_id')
    ref = fields.Char(default='New')
    create_time = fields.Datetime(readonly=1, default=fields.Datetime.now())
    next_time = fields.Datetime(compute='_compute_next_time')

    _sql_constraints = [('unique_name', 'unique("name")', 'This name already exists')]

    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price

    @api.depends('create_time')  # ✅ تم تعديل الـ depends هنا
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time = rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False  # للتأكد من أن الحقل لا يُترك بدون قيمة

    @api.model_create_multi
    def create(self, vals_list):
        records = super(Property, self).create(vals_list)
        for record in records:
            if record.ref == 'New':
                record.ref = self.env['ir.sequence'].next_by_code('property_squ')
        return records

    def create_history(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property_history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'lines_ids': [
                    (0, 0, {
                        'description': line.description,
                        'area': line.area
                    }) for line in rec.line_ids
                ]
            })

    def check_expected_selling_date(self):
        property_id = self.search([])
        for rec in property_id:
            if rec.expected_selling_date and rec.expected_selling_date < fields.Date.today():
                rec.is_late = True

    @api.constrains('bedrooms')
    def _check_bedrooms_greeter_zero(self):
        for rec in self:
            if rec.expected_price == 0:
                raise ValidationError('Please enter a value for bedroom')

    @api.constrains('age')
    def _check_age_greeter_zero(self):
        for rec in self:
            if rec.selling_price == 0:
                raise ValidationError('Please add a value for age')

    def action_draft(self):
        for rec in self:
            rec.create_history(rec.state, 'draft')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.create_history(rec.state, 'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_history(rec.state, 'sold')
            rec.state = 'sold'

    def action_close(self):
        for rec in self:
            rec.create_history(rec.state, 'close')
            rec.state = 'close'

    def action_open_change_state(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def action(self):
        print(self.env['property'].search(['|',('name','=','property1'),('postcode','=','PH011')]))

    def action_open_related_owner(self):
        print("action_open_related_owner")
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_form_view').id
        action['res_id'] = self.owner_id.id
        action['views'] =  [[view_id,'form']]
        return action

class PropertyLines(models.Model):
    _name = 'property.lines'
    property_id = fields.Many2one('property')
    description = fields.Char()
    area = fields.Float()
