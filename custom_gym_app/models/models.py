# -*- coding: utf-8 -*-
import uuid
from werkzeug.urls import url_encode
from odoo import models, fields, api


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    member_status = fields.Selection([('draft', "Draft"), ('approved', "Approved")], group_expand='_expand_member_status', default='draft', string='Member Status')

    national_id = fields.Char(string='National ID')
    birth_date = fields.Date(string='Birth Date')
    nationality = fields.Many2one('res.country', string='Nationality')
    member_selection = fields.Selection(selection=[('arabic', 'عضوية شركاء النجاح')], string="Member")

    access_token = fields.Char('Security Token', copy=False)
    gym_type = fields.Selection([('trainer', "Trainer"), ('member', "Member")], string='User Type')

    def create(self, values):
        res = super(ResPartnerInherit, self).create(values)
        if res.member_selection == 'arabic':
            member_pricelist = self.env['product.pricelist'].search([('name', 'like', 'Successful Member Pricelist')])
            if member_pricelist:
                res.property_product_pricelist = member_pricelist
        return res

    @api.onchange('member_selection')
    def _onchange_member_selection(self):
        for rec in self:
            if rec.member_selection == 'arabic':
                member_pricelist = self.env['product.pricelist'].search([('name', 'like', 'Successful Member Pricelist')])
                if member_pricelist:
                    rec.property_product_pricelist = member_pricelist

    def write(self, values):
        res = super(ResPartnerInherit, self).write(values)

        if values.get('member_status'):
            if values['member_status'] == 'approved':
                user_obj = self.env['res.users']
                group_portal = self.env.ref('base.group_portal')
                partner_id = self.env['res.partner'].search([('name', '=', self.name)])

                values_user = {
                                'name': self.name,
                                'login': self.email,
                                'email': self.email,
                                'active': True,
                                'groups_id': [(4, group_portal.id)],
                                'partner_id': partner_id.id,
                              }

                user_obj.sudo().create(values_user)
                user_obj.sudo().action_reset_password()
                print('MEMBER STATUS APPROVED')

        return res

    def _expand_member_status(self, states, domain, order):
        return [key for key, val in type(self).member_status.selection]

    def _portal_ensure_token(self):
        """ Get the current record access token """
        if not self.access_token:
            self.sudo().write({'access_token': str(uuid.uuid4())})
        return self.access_token

    def get_portal_url(self, membership_id, report_type=None, download=None, query_string=None, anchor=None):
        self.ensure_one()
        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/my/membership/' + '%s?access_token=%s%s%s' % (membership_id if membership_id else '', self._portal_ensure_token(), '&report_type=%s' % report_type if report_type else '', '&download=true' if download else '')
        return url

    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s' % self.name


class PlanningSlotInherit(models.Model):
    _inherit = 'planning.slot'

    access_token = fields.Char('Security Token', copy=False)

    def _portal_ensure_token(self):
        """ Get the current record access token """
        if not self.access_token:
            self.sudo().write({'access_token': str(uuid.uuid4())})
        return self.access_token

    def get_portal_url(self, schedule_id, report_type=None, download=None, query_string=None, anchor=None):
        self.ensure_one()
        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/my/schedule/' + '%s?access_token=%s%s%s' % (schedule_id if schedule_id else '', self._portal_ensure_token(), '&report_type=%s' % report_type if report_type else '', '&download=true' if download else '')
        return url

    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s %s' % (self.employee_id.name, self.start_datetime)
