import io
import json
import xlsxwriter
from dateutil.utils import today
from odoo import fields, models
from odoo.tools.json import json_default
from datetime import datetime


class LeaveReport(models.TransientModel):
    """This model is used for get the data for leave report from wizard."""

    _name = 'leave.report'
    _description = "Leave Report Wizard"

    report_type = fields.Selection([('month','Month'),('week','Week'),('day','Day'),('custom','Custom')],
                                   string='Report Type')
    start_date = fields.Datetime(default=today())
    end_date = fields.Datetime(default=today())
    based_on = fields.Selection([('class','Class'),('student','Student')], string='Based On', required=True)
    selected_class_ids = fields.Many2many('school.class', string='Class')
    selected_students_ids = fields.Many2many('student.registration', string='Student')

    def action_leave_print_pdf_report(self):
        """Method used for get values from wizard to return it to the abstract model."""

        data = {
            'report_type': self.report_type,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'based_on': self.based_on,
            'selected_class_ids': self.selected_class_ids.ids,
            'selected_students_ids': self.selected_students_ids.ids
        }
        return self.env.ref('school.action_leave_report').report_action(None, data=data)


    def action_leave_print_xls_report(self):
        """Method used for get values from wizard to return it to the abstract model."""

        wizard_data = self.action_leave_print_pdf_report()
        data = wizard_data['data']
        fetched_data = self.env['report.school.leave_report_template']
        result_data = fetched_data._get_report_values(self, data=data)

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'leave.report',
                     'options': json.dumps(result_data,
                                           default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Leave Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """Method used to design the xlsx sheet for the fetched data."""

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px', 'align': 'center'})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        current_date = datetime.today().strftime('%y-%m-%d')
        company = self.env.company.name

        sheet.merge_range('C2:C3', 'Report Print Date', txt)
        sheet.merge_range('G2:G3', 'Company Name', txt)
        sheet.write('C4:C4', current_date, txt)
        sheet.write('G4:G4', company, txt)
        sheet.merge_range('D2:F3', 'LEAVE REPORT', head)
        if data['report_type'] == 'Class Wise Report':
            sheet.merge_range('D4:F4', 'CLASS WISE REPORT', txt)
            row = 6
            col = 1
            sheet.set_column(2,2, 20)
            sheet.set_column(3,3, 20)
            sheet.set_column(4,4, 20)
            sheet.set_column(5,5, 20)
            sheet.set_column(6,6, 20)
            for class_index,(class_name,students) in enumerate(data['report'].items()):
                row += 1
                sheet.write(row,col + 1, f"Class:{class_name}", cell_format)
                row += 1
                sheet.write(row,col + 1, 'Registration No', txt)
                sheet.write(row,col + 2, 'Name', txt)
                sheet.write(row,col + 3, 'Last Name', txt)
                sheet.write(row,col + 4, 'Start Date', txt)
                sheet.write(row,col + 5, 'End Date', txt)
                sheet.write(row,col + 6, 'Reason', txt)
                row += 1
                for student in students:
                    sheet.write(row,col + 1, f'{student['registration_no']}',txt)
                    sheet.write(row,col + 2, f'{student['name']}',txt)
                    sheet.write(row,col + 3, f'{student['last_name']}',txt)
                    sheet.write(row,col + 4, f'{student['start_date']}',txt)
                    sheet.write(row,col + 5, f'{student['end_date']}',txt)
                    sheet.write(row,col + 6, f'{student['reason']}',txt)
                    row +=1
            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()

        elif data['report_type'] == 'Student Wise Report':
            sheet.merge_range('D4:F4', 'STUDENT WISE REPORT', txt)
            row = 6
            col = 1
            sheet.set_column(2,2, 20)
            sheet.set_column(3,3, 20)
            sheet.set_column(4,4, 20)
            sheet.set_column(5,5, 20)
            sheet.set_column(6,6, 20)
            for class_index,(class_name,students) in enumerate(data['report'].items()):
                row += 1
                sheet.write(row,col + 1, f"Name:{class_name}", cell_format)
                row += 1
                sheet.write(row,col + 1, 'Registration No', txt)
                sheet.write(row,col + 2, 'Start Date', txt)
                sheet.write(row,col + 3, 'End Date', txt)
                sheet.write(row,col + 4, 'Class', txt)
                row += 1
                for student in students:
                    sheet.write(row,col + 1, f'{student['registration_no']}',txt)
                    sheet.write(row,col + 2, f'{student['start_date']}',txt)
                    sheet.write(row,col + 3, f'{student['end_date']}',txt)
                    sheet.write(row,col + 4, f'{student['class_name']}',txt)
                    row +=1
            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()
        else:
            pass

    def cancel(self):
        print('canceled')

