# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class MembersController(http.Controller):
    @http.route('/member_registration', type='http', auth="public", website=True)
    def member_registration_page(self, **kw):
        countries = request.env['res.country'].search([])
        return http.request.render('custom_gym_app.member_registration_page_template', {'countries': countries})

    @http.route('/create/member', type='http', auth="public", website=True)
    def create_member(self, **kwargs):
        kwargs['category_id'] = request.env['res.partner.category'].sudo().search(['|',('name','=','Gym'),('name','=','gym')])
        kwargs['gym_type'] = 'member'
        kwargs['member_status'] = 'draft'
        request.env['res.partner'].sudo().create(kwargs)
        return request.render('custom_gym_app.member_registration_page_template', {})


# class WebsiteShopInheritance(WebsiteSale):
#     @http.route([
#         '''/shop''',
#         '''/shop/page/<int:page>''',
#         '''/shop/subscription_type/<string:subscription_type>''',
#         '''/shop/category/<model("product.public.category"):category>''',
#         '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
#     ], type='http', auth="public", website=True)
#     def shop(self, page=0, subscription_type=None, category=None, search='', ppg=False, **post):
#         res = super(WebsiteShopInheritance, self).shop(page=0, category=None, search='', ppg=False, **post)
#         print('POST IS: ', subscription_type)
#         if subscription_type == 'monthly':
#             res.qcontext["subscription_type"] = 'monthly'
#         if subscription_type == 'yearly':
#             res.qcontext["subscription_type"] = 'yearly'
#         if subscription_type == 'weekly':
#             res.qcontext["subscription_type"] = 'weekly'
#         return res
