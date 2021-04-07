# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartnerInheritanceSchool(models.Model):
    _inherit = 'res.partner'

    school_member = fields.Boolean(string='School Member', default=False)

    year = fields.Integer(string='Year', required=True)
    semester = fields.Selection([('opt_1', 'الفصل الدراسي الاول'), ('opt_2', 'الفصل الدراسي الثاني'), ('opt_3', 'الفصل الصيفي')], string='Semester', required=True)
    student_birthday = fields.Date(string='Birth Date', required=True)
    id_resource = fields.Integer(string='ID Resource', required=True)
    work_place = fields.Char(string='Workplace', required=True)
    neighbourhood = fields.Char(string='Neighbourhood', required=True)
    beside = fields.Char(string='Beside')
    grade = fields.Char(string='Grade', required=True)
    birth_place = fields.Many2one('res.country', string='Birth Place', required=True)
    id_date = fields.Date(string='ID Date', required=True)

    student_class = fields.Char(string='Class', required=True)
    father_name = fields.Char(string='Father Name', required=True)
    student_id = fields.Integer(string='Student ID', required=True)
    father_job = fields.Char(string='Father Job', required=True)
    school_transferred_from = fields.Char(string='Transferred From')
    no_of_responsible = fields.Char(string="Responsible", required=True)
