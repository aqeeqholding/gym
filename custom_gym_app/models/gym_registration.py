# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartnerInheritance(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
