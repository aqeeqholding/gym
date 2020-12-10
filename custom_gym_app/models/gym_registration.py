# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartnerInheritance(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'


class SaleSubscriptionInheritance(models.Model):
    _name = 'sale.subscription'
    _inherit = 'sale.subscription'


class PlanningSlotInheritance(models.Model):
    _name = 'planning.slot'
    _inherit = 'planning.slot'
