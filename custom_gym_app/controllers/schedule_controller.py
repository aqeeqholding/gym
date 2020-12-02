# -*- coding: utf-8 -*-

from odoo import fields, http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError

from collections import OrderedDict
from dateutil.relativedelta import relativedelta

from odoo.http import request
from odoo.tools import date_utils
from odoo.osv.expression import AND, OR


class PortalSchedule(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if 'schedule_count' in counters:
            logged_in_user = request.env['res.users'].browse([request.session.uid])

            schedule_count = 0

            if logged_in_user.partner_id.gym_type:
                if logged_in_user.partner_id.gym_type == 'trainer':
                    schedule_count = request.env['planning.slot'].sudo().search_count([('employee_id.name', '=', logged_in_user.name)])
                elif logged_in_user.partner_id.gym_type == 'member':
                    schedule_count = request.env['planning.slot'].sudo().search_count([])
            else:
                schedule_count = request.env['planning.slot'].sudo().search_count([])

            values['schedule_count'] = schedule_count

        return values

    def _schedule_get_page_view_values(self, schedule, access_token, **kwargs):
        values = {
                    'page_name': 'schedule',
                    'schedule': schedule,
                 }
        return self._get_page_view_values(schedule, access_token, values, 'my_schedule_history', False, **kwargs)

    @http.route(['/my/schedule', '/my/schedule/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_schedule(self, page=1, date_begin=None, date_end=None, sortby=None, search=None, search_in='name', filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        Schedule = request.env['planning.slot']

        domain = []

        logged_in_user = request.env['res.users'].browse([request.session.uid])

        if logged_in_user.partner_id.gym_type:
            if logged_in_user.partner_id.gym_type == 'trainer':
                domain += [('user_id.name', '=', logged_in_user.name), ('employee_id.name', '=', logged_in_user.name)]

        today = fields.Date.today()
        quarter_start, quarter_end = date_utils.get_quarter(today)
        last_week = today + relativedelta(weeks=-1)
        last_month = today + relativedelta(months=-1)
        last_year = today + relativedelta(years=-1)

        searchbar_filters = {
                                'all': {'label': _('All'), 'domain': []},
                                'today': {'label': _('Today'), 'domain': [("start_datetime", "=", fields.Date.today())]},
                                'week': {'label': _('This week'), 'domain': [('start_datetime', '>=', date_utils.start_of(today, "week")), ('end_datetime', '<=', date_utils.end_of(today, 'week'))]},
                                'month': {'label': _('This month'), 'domain': [('start_datetime', '>=', date_utils.start_of(today, 'month')), ('end_datetime', '<=', date_utils.end_of(today, 'month'))]},
                                'year': {'label': _('This year'), 'domain': [('start_datetime', '>=', date_utils.start_of(today, 'year')), ('end_datetime', '<=', date_utils.end_of(today, 'year'))]},
                                'quarter': {'label': _('This Quarter'), 'domain': [('start_datetime', '>=', quarter_start), ('end_datetime', '<=', quarter_end)]},
                                'last_week': {'label': _('Last week'), 'domain': [('start_datetime', '>=', date_utils.start_of(last_week, "week")), ('end_datetime', '<=', date_utils.end_of(last_week, 'week'))]},
                                'last_month': {'label': _('Last month'), 'domain': [('start_datetime', '>=', date_utils.start_of(last_month, 'month')), ('end_datetime', '<=', date_utils.end_of(last_month, 'month'))]},
                                'last_year': {'label': _('Last year'), 'domain': [('start_datetime', '>=', date_utils.start_of(last_year, 'year')), ('end_datetime', '<=', date_utils.end_of(last_year, 'year'))]},
                            }

        if not filterby:
            filterby = 'all'

        domain = AND([domain, searchbar_filters[filterby]['domain']])

        searchbar_inputs = {
                                'name': {'input': 'name', 'label': _('Search Name')},
                                'trainer': {'input': 'trainer', 'label': _('Search Trainer')},
                                'role': {'input': 'role', 'label': _('Search Role')},
                            }

        if search and search_in:
            search_domain = []
            if search_in in 'name':
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in 'trainer':
                search_domain = OR([search_domain, [('employee_id.name', 'ilike', search)]])
            if search_in in 'role':
                search_domain = OR([search_domain, [('role_id.name', 'ilike', search)]])

            domain += search_domain

        schedule_count = Schedule.sudo().search_count(domain)

        pager = portal_pager(
                                url="/my/schedule",
                                url_args={'date_begin': date_begin, 'date_end': date_end, 'search_in': search_in, 'search': search, 'sortby': sortby, 'filterby': filterby},
                                total=schedule_count,
                                page=page,
                                step=self._items_per_page
                            )

        schedules = Schedule.sudo().search(domain, order=None, limit=self._items_per_page, offset=pager['offset'])

        request.session['my_schedule_history'] = schedules.ids[:100]

        values.update({
                            'date': date_begin,
                            'schedules': schedules,
                            'page_name': 'schedule',
                            'pager': pager,
                            'default_url': '/my/schedule',
                            'sortby': sortby,
                            'search_in': search_in,
                            'search': search,
                            'searchbar_inputs': searchbar_inputs,
                            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                            'filterby': filterby,
                     })
        return request.render("custom_gym_app.portal_my_schedule", values)

    @http.route(['/my/schedule/<int:schedule_id>'], type='http', auth="public", website=True)
    def portal_my_schedule_detail(self, schedule_id, access_token=None, report_type=None, download=False, **kw):
        try:
            schedule_sudo = self._document_check_access('planning.slot', schedule_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=schedule_sudo, report_type=report_type, report_ref='custom_gym_app.report_schedule_card', download=download)

        values = self._schedule_get_page_view_values(schedule_sudo, access_token, **kw)

        return request.render("custom_gym_app.portal_my_schedule_page", values)
