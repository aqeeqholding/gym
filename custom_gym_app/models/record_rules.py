# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartnerInheritRules(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, values_list):
        flag = self.env['res.users'].has_group('custom_gym_app.customer_service_edit_members')
        if not flag:
            res = super(ResPartnerInheritRules, self).create(values_list)
            return res
        else:
            raise ValidationError(_("Sorry, Customer Services Representative Not Allowed To Create Members"))

    def unlink(self):
        flag = self.env['res.users'].has_group('custom_gym_app.customer_service_edit_members')
        if not flag:
            res = super(ResPartnerInheritRules, self).unlink()
            return res
        else:
            raise ValidationError(_("Sorry, Customer Services Representative Not Allowed To Delete Members"))


class SaleSubscriptionInheritRules(models.Model):
    _inherit = 'sale.subscription'

    @api.model
    def create(self, values_list):
        flag = self.env['res.users'].has_group('custom_gym_app.customer_service_edit_subscription')
        if not flag:
            res = super(SaleSubscriptionInheritRules, self).create(values_list)
            return res
        else:
            raise ValidationError(_("Sorry, Customer Services Representative Not Allowed To Create Subscriptions"))

    def unlink(self):
        flag = self.env['res.users'].has_group('custom_gym_app.customer_service_edit_subscription')
        if not flag:
            res = super(SaleSubscriptionInheritRules, self).unlink()
            return res
        else:
            raise ValidationError(_("Sorry, Customer Services Representative Not Allowed To Delete Subscriptions"))


class PlanningSlotInheritRules(models.Model):
    _inherit = 'planning.slot'

    @api.model
    def create(self, values_list):
        flag = self.env['res.users'].has_group('custom_gym_app.customer_service_view_planning')
        if not flag:
            res = super(PlanningSlotInheritRules, self).create(values_list)
            return res
        else:
            raise ValidationError(_("Sorry, Customer Services Representative Not Allowed To Create Planning"))

    def unlink(self):
        flag = self.env['res.users'].has_group('custom_gym_app.customer_service_view_planning')
        if not flag:
            res = super(PlanningSlotInheritRules, self).unlink()
            return res
        else:
            raise ValidationError(_("Sorry, Customer Services Representative Not Allowed To Delete Planning"))

    def write(self, values_list):
        flag = self.env['res.users'].has_group('custom_gym_app.customer_service_view_planning')
        if not flag:
            res = super(PlanningSlotInheritRules, self).write(values_list)
            return res
        else:
            raise ValidationError(_("Sorry, Customer Services Representative Not Allowed To Edit Planning"))


class ResUsersInheritRules(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, values_list):
        flag = self.env['res.users'].has_group('custom_gym_app.customer_service_edit_portal_management')
        if not flag:
            res = super(ResUsersInheritRules, self).create(values_list)
            return res
        else:
            raise ValidationError(_("Sorry, Customer Services Representative Not Allowed To Create User"))

    def unlink(self):
        flag = self.env['res.users'].has_group('custom_gym_app.customer_service_edit_portal_management')
        if not flag:
            res = super(ResUsersInheritRules, self).unlink()
            return res
        else:
            raise ValidationError(_("Sorry, Customer Services Representative Not Allowed To Delete User"))


class ResPartnerInheritRulesReception(models.Model):
    _inherit = 'res.partner'

    def unlink(self):
        flag = self.env['res.users'].has_group('custom_gym_app.reception_create_edit_members')
        if not flag:
            res = super(ResPartnerInheritRulesReception, self).unlink()
            return res
        else:
            raise ValidationError(_("Sorry, Reception User Not Allowed To Delete Member"))


class SaleSubscriptionInheritRulesReception(models.Model):
    _inherit = 'sale.subscription'

    def unlink(self):
        flag = self.env['res.users'].has_group('custom_gym_app.reception_create_edit_subscription')
        if not flag:
            res = super(SaleSubscriptionInheritRulesReception, self).unlink()
            return res
        else:
            raise ValidationError(_("Sorry, Reception User Not Allowed To Delete Subscription"))


class ViewPlanningInheritRulesReception(models.Model):
    _inherit = 'planning.slot'

    @api.model
    def create(self, values_list):
        flag = self.env['res.users'].has_group('custom_gym_app.reception_view_planning')
        if not flag:
            res = super(ViewPlanningInheritRulesReception, self).create(values_list)
            return res
        else:
            raise ValidationError(_("Sorry, Reception User Not Allowed To Create Planning"))

    def write(self, values_list):
        flag = self.env['res.users'].has_group('custom_gym_app.reception_view_planning')
        if not flag:
            res = super(ViewPlanningInheritRulesReception, self).write(values_list)
            return res
        else:
            raise ValidationError(_("Sorry, Reception User Not Allowed To Edit Planning"))

    def unlink(self):
        flag = self.env['res.users'].has_group('custom_gym_app.reception_view_planning')
        if not flag:
            res = super(ViewPlanningInheritRulesReception, self).unlink()
            return res
        else:
            raise ValidationError(_("Sorry, Reception User Not Allowed To Delete Planning"))


class AccountMoveInheritRulesReception(models.Model):
    _inherit = 'account.move'

    def write(self, values_list):
        flag = self.env['res.users'].has_group('custom_gym_app.reception_create_invoice')
        if not flag:
            res = super(AccountMoveInheritRulesReception, self).write(values_list)
            return res
        else:
            raise ValidationError(_("Sorry, Reception User Not Allowed To Edit Invoice"))

    def unlink(self):
        flag = self.env['res.users'].has_group('custom_gym_app.reception_create_invoice')
        if not flag:
            res = super(AccountMoveInheritRulesReception, self).unlink()
            return res
        else:
            raise ValidationError(_("Sorry, Reception User Not Allowed To Delete Invoice"))


class ResUsersInheritRulesReception(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, values_list):
        flag = self.env['res.users'].has_group('custom_gym_app.reception_edit_portal_management')
        if not flag:
            res = super(ResUsersInheritRulesReception, self).create(values_list)
            return res
        else:
            raise ValidationError(_("Sorry, Reception User Not Allowed To Create Portal User"))

    def unlink(self):
        flag = self.env['res.users'].has_group('custom_gym_app.reception_edit_portal_management')
        if not flag:
            res = super(ResUsersInheritRulesReception, self).unlink()
            return res
        else:
            raise ValidationError(_("Sorry, Reception User Not Allowed To Delete Portal User"))


class PlanningSlotInheritRulesChef(models.Model):
    _inherit = 'planning.slot'

    def unlink(self):
        flag = self.env['res.users'].has_group('custom_gym_app.chef_trainers_create_edit_planning')
        if not flag:
            res = super(PlanningSlotInheritRulesChef, self).unlink()
            return res
        else:
            raise ValidationError(_("Sorry, Chef Trainer Not Allowed To Delete Planning Slot"))
