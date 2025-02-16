from odoo import models,api,fields
from odoo.tools import date_utils


class ReportSchoolLeaveReportTemplate(models.AbstractModel):
    _name = 'report.school.leave_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Method used for execute queries based on the wizard data and return to the template."""

        query = """ SELECT sr.registration_no, sr.name, sr.last_name,
                            sl.start_date,sl.end_date,sl.reason,
        					sc.name as class_name
                            FROM school_leave sl
                            INNER JOIN student_registration sr ON sr.id = sl.student_id
        					INNER JOIN school_class sc ON sc.id = sr.class_id
        					"""
        # Check Report Type

        if data['report_type'] == 'month':
            today = fields.date.today()
            current_month = date_utils.subtract(today, months=0)
            starting_current_month = date_utils.start_of(current_month, "month")
            ending_current_month = date_utils.end_of(current_month, "month")
            query += """ where sl.start_date >= '%s' and sl.end_date <= '%s'""" % (
            starting_current_month, ending_current_month)
            self.env.cr.execute(query)
        elif data['report_type'] == 'week':
            today = fields.date.today()
            starting_current_week = date_utils.start_of(today, "week")
            ending_current_week = date_utils.end_of(today, "week")
            query += """ where sl.start_date >= '%s' and sl.end_date <= '%s'""" % (
            starting_current_week, ending_current_week)
            self.env.cr.execute(query)
        elif data['report_type'] == 'day':
            today = fields.date.today()
            start_date = today
            end_date = today
            query += """ where sl.start_date >= '%s' and sl.end_date <= '%s'""" % (start_date, end_date)
            self.env.cr.execute(query)
        elif data['report_type'] == 'custom':
            start_date = data['start_date']
            end_date = data['end_date']
            query += """ where sl.start_date >= '%s' and sl.end_date <= '%s'""" % (start_date, end_date)
            self.env.cr.execute(query)
        else:
            query += """"""

        # Check Based on

        if data['based_on'] == 'class':
            if data['selected_class_ids']:
                query += """and sc.id in %s order by sc.id"""
                params = [tuple(data['selected_class_ids'])]
                self.env.cr.execute(query, params)
                report_data = self.env.cr.dictfetchall()

                class_wise_report = {}
                for student in report_data:
                    class_name = student.pop('class_name')
                    if class_name not in class_wise_report:
                        class_wise_report[class_name] = []
                    class_wise_report[class_name].append(student)

                data = {'report': class_wise_report,
                        'report_type': 'Class Wise Report'}
            else:
                query += """ order by sc.id"""
                self.env.cr.execute(query)
                report_data = self.env.cr.dictfetchall()

                class_wise_report = {}
                for student in report_data:
                    class_name = student.pop('class_name')
                    if class_name not in class_wise_report:
                        class_wise_report[class_name] = []
                    class_wise_report[class_name].append(student)

                data = {'report': class_wise_report,
                        'report_type': 'Class Wise Report'}

        elif data['based_on'] == 'student':
            if data['selected_students_ids']:
                query += """and sr.id in %s"""
                params = [tuple(data['selected_students_ids'])]
                self.env.cr.execute(query, params)
                report_data = self.env.cr.dictfetchall()

                student_wise_report = {}
                for student in report_data:
                    name = student.pop('name')
                    if name not in student_wise_report:
                        student_wise_report[name] = []
                    student_wise_report[name].append(student)

                data = {'report': student_wise_report,
                        'report_type': 'Student Wise Report'}
            else:
                query += """ order by sr.id """
                self.env.cr.execute(query)
                report_data = self.env.cr.dictfetchall()

                student_wise_report = {}
                for student in report_data:
                    name = student.pop('name')
                    if name not in student_wise_report:
                        student_wise_report[name] = []
                    student_wise_report[name].append(student)

                data = {'report': student_wise_report,
                        'report_type': 'Student Wise Report'}
        return data
