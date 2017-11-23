# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from datetime import datetime
import time
#Import logger
import logging
#Get the logger
logger = logging.getLogger(__name__)
from odoo import models, api


class ReportMarksheetFinalReport(models.AbstractModel):
    _name = 'report.openeducat_exam.report_marksheet_final_report'

    def get_objects_new(self, objects):
        obj = []
        for object in objects:
            obj.extend(object)
        return obj

    def get_lines_new(self, obj):
        lines = []
        lines_all = self.env['op.marksheet.line'].search(
                        [('exam_session_id', 'in', obj.exam_session_id.ids)])
        student_lines = {}
        for line in lines_all:
            logger.info(line.student_id.id)
            if line.student_id.id in student_lines.keys():
                student_lines[line.student_id.id].append(line)
            else:
                student_lines[line.student_id.id] = [line]
        lines = [student_lines[key] for key in student_lines]
        return lines

    def get_student_name(self, lines):
        for line in lines:
            return "{} {} {}".format(line.student_id.name, line.student_id.middle_name, line.student_id.last_name).replace('  ', ' ')


    def get_course_name(self, lines):
        for line in lines:
            return line.marksheet_reg_id.exam_session_id.course_id.name

    def get_all_session_names(self, obj):
        session_name = []
        for session in obj.exam_session_id:
            session_name.append(session.name)
        return session_name

    def get_calspan(self, obj):
        session_name = self.get_all_session_names(obj)
        return len(session_name) + 2


    def get_date_new(self, date):
        date1 = datetime.strptime(date, "%Y-%m-%d")
        return str(date1.month) + ' / ' + str(date1.year)

    def get_total_new(self, marksheet_line):
        total = [x.exam_id.total_marks for x in marksheet_line.result_line]
        return sum(total)

    @api.model
    def get_report_values(self, docids, data=None):
        docs_new = self.env['op.marksheet.final'].browse(docids)
        docargs = {
            'doc_model': 'op.marksheet.final',
            'docs_new': docs_new,
            'time': time,
            'get_objects_new': self.get_objects_new,
            'get_lines_new': self.get_lines_new,
            'get_date_new': self.get_date_new,
            'get_total_new': self.get_total_new,
            'get_student_name': self.get_student_name,
            'get_course_name': self.get_course_name,
            'get_all_session_names': self.get_all_session_names,
            'get_calspan': self.get_calspan,
        }
        return docargs
