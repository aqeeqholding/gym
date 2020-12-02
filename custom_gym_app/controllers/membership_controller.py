# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request


class PortalMembership(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if 'membership_count' in counters:
            logged_in_user = request.env['res.users'].browse([request.session.uid])

            membership_count = request.env['res.partner'].search_count([('user_ids', '=', logged_in_user.id)])
            values['membership_count'] = membership_count

        return values

    def _membership_get_page_view_values(self, membership, access_token, **kwargs):
        values = {
                    'page_name': 'membership',
                    'membership': membership,
                 }
        return self._get_page_view_values(membership, access_token, values, 'my_membership_history', False, **kwargs)

    @http.route(['/my/membership', '/my/membership/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_membership(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        Membership = request.env['res.partner']

        logged_in_user = request.env['res.users'].browse([request.session.uid])

        membership_count = Membership.search_count([('user_ids', '=', logged_in_user.id)])

        pager = portal_pager(
                                url="/my/membership",
                                url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
                                total=membership_count,
                                page=page,
                                step=self._items_per_page
                            )

        memberships = Membership.search([('user_ids', '=', logged_in_user.id)], order=None, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_membership_history'] = memberships.ids[:100]

        values.update({
                            'date': date_begin,
                            'memberships': memberships,
                            'page_name': 'membership',
                            'pager': pager,
                            'default_url': '/my/membership',
                            'sortby': sortby,
                            'filterby': filterby,
                     })
        return request.render("custom_gym_app.portal_my_membership", values)

    @http.route(['/my/membership/<int:membership_id>'], type='http', auth="public", website=True)
    def portal_my_membership_detail(self, membership_id, access_token=None, report_type=None, download=False, **kw):
        try:
            membership_sudo = self._document_check_access('res.partner', membership_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=membership_sudo, report_type=report_type, report_ref='custom_gym_app.report_member_card', download=download)

        values = self._membership_get_page_view_values(membership_sudo, access_token, **kw)

        return request.render("custom_gym_app.portal_my_membership_page", values)
