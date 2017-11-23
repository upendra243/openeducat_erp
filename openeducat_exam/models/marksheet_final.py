# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpMarksheetFinal(models.Model):
    _name = 'op.marksheet.final'
    _inherit = ['mail.thread']

    exam_session_id = fields.Many2many(
        'op.exam.session', string='Exam Sessions',
        required=True, track_visibility='onchange')
    generated_date = fields.Date(
        'Generated Date', required=True,
        default=fields.Date.today(), track_visibility='onchange')
    generated_by = fields.Many2one(
        'res.users', 'Generated By',
        default=lambda self: self.env.uid,
        required=True, track_visibility='onchange')
    status = fields.Selection(
        [('draft', 'Draft'), ('validated', 'Validated'),
         ('cancelled', 'Cancelled')], 'Status',
        default="draft", required=True, track_visibility='onchange')
    total_pass = fields.Integer(
        'Total Pass', compute='_compute_total_pass',
        track_visibility='onchange')
    total_failed = fields.Integer(
        'Total Fail', compute='_compute_total_failed',
        track_visibility='onchange')
    name = fields.Char('Marksheet Final', size=256, required=True,
                       track_visibility='onchange')
    result_template_id = fields.Many2one(
        'op.result.template', 'Result Template',
        required=True, track_visibility='onchange')

    @api.constrains('total_pass', 'total_failed')
    def _check_marks(self):
        if (self.total_pass < 0.0) or (self.total_failed < 0.0):
            raise ValidationError(_('Enter proper pass or fail!'))

    @api.multi
    def _compute_total_pass(self):
        self.total_pass = 10

    @api.multi
    def _compute_total_failed(self):
        self.total_failed = 5
