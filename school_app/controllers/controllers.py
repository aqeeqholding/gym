# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class SchoolMembersController(http.Controller):
    @http.route('/school/registration', type='http', auth="public", website=True)
    def school_registration_page(self, **kw):
        countries = request.env['res.country'].search([])
        return http.request.render('school_app.school_registration_page_template', {'countries': countries})

    @http.route('/create/school/member', type='http', auth="public", website=True)
    def create_school_member(self, **kwargs):
        kwargs['school_member'] = True
        request.env['res.partner'].sudo().create(kwargs)
        countries = request.env['res.country'].search([])
        return request.render('school_app.school_registration_page_template', {'countries': countries})