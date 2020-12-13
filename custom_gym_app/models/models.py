# -*- coding: utf-8 -*-
import uuid
from werkzeug.urls import url_encode
from odoo import models, fields, api


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    national_id = fields.Char(string='National ID')
    birth_date = fields.Date(string='Birth Date')
    nationality = fields.Char(string='Nationality')

    access_token = fields.Char('Security Token', copy=False)
    gym_type = fields.Selection([('trainer', "Trainer"), ('member', "Member")], string='User Type')

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
