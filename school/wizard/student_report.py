import io
import json
import xlsxwriter
from odoo import fields, models
from odoo.tools.json import json_default
from datetime import datetime

class StudentReport(models.TransientModel):
    """This model is used for get the data for student report from wizard."""

    _name = 'student.report'
    _description = "Student Report Wizard"

    report_type = fields.Selection([('class','Class'),('department','Department'),('club','Club')],
                                   string='Report Type')
    selected_class_ids = fields.Many2many('school.class', string='Class')
    selected_department_ids = fields.Many2many('school.department', string='Department')
    selected_clubs_ids = fields.Many2many('school.club', string='Club')

    def action_student_print_pdf_report(self):
        """Method used for get values from wizard to return it to the abstract model."""

        data = {
            'report_type': self.report_type,
            'selected_class_ids': self.selected_class_ids.ids,
            'selected_department_ids': self.selected_department_ids.ids,
            'selected_clubs_ids': self.selected_clubs_ids.ids
        }
        return self.env.ref('school.action_student_report').report_action(None, data=data)

    def action_student_print_xls_report(self):
        """Method used for get values from wizard to return it to the abstract model."""

        wizard_data = self.action_student_print_pdf_report()
        data = wizard_data['data']
        fetched_data = self.env['report.school.student_report_template']
        result_data = fetched_data._get_report_values(self, data=data)

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'student.report',
                     'options': json.dumps(result_data,
                                           default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Student Excel Report',
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

        sheet.merge_range('D2:F3', 'STUDENT REPORT', head)
        if data['report_type'] == 'Class Wise Report':
            sheet.merge_range('D4:F4', 'CLASS WISE REPORT', txt)
            row = 5
            col = 1
            sheet.set_column(2, 2, 20)
            sheet.set_column(3, 3, 20)
            sheet.set_column(4, 4, 20)
            sheet.set_column(5, 5, 20)
            sheet.set_column(6, 6, 20)
            for class_index, (class_name, students) in enumerate(data['report'].items()):
                row += 1
                sheet.write(row, col + 1, f"Class:{class_name}", cell_format)
                row += 1
                sheet.write(row, col + 1, 'Registration No', txt)
                sheet.write(row, col + 2, 'Name', txt)
                sheet.write(row, col + 3, 'Last Name', txt)
                sheet.write(row, col + 4, 'email', txt)
                row += 1
                for student in students:
                    sheet.write(row, col + 1, f'{student['registration_no']}', txt)
                    sheet.write(row, col + 2, f'{student['name']}', txt)
                    sheet.write(row, col + 3, f'{student['last_name']}', txt)
                    sheet.write(row, col + 4, f'{student['email']}', txt)
                    row += 1
            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()

        elif data['report_type'] == 'Department Wise Report':
            sheet.merge_range('D4:F4', 'DEPARTMENT WISE REPORT', txt)
            row = 5
            col = 1
            sheet.set_column(2, 2, 20)
            sheet.set_column(3, 3, 20)
            sheet.set_column(4, 4, 20)
            sheet.set_column(5, 5, 20)
            sheet.set_column(6, 6, 20)
            for class_index, (class_name, students) in enumerate(data['report'].items()):
                row += 1
                sheet.write(row, col + 1, f"Class:{class_name}", cell_format)
                row += 1
                sheet.write(row, col + 1, 'Registration No', txt)
                sheet.write(row, col + 2, 'Name', txt)
                sheet.write(row, col + 3, 'Last Name', txt)
                sheet.write(row, col + 4, 'email', txt)
                row += 1
                for student in students:
                    sheet.write(row, col + 1, f'{student['registration_no']}', txt)
                    sheet.write(row, col + 2, f'{student['name']}', txt)
                    sheet.write(row, col + 3, f'{student['last_name']}', txt)
                    sheet.write(row, col + 4, f'{student['email']}', txt)
                    row += 1
            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()

        elif data['report_type'] == 'Club Wise Report':
            sheet.merge_range('D4:F4', 'CLUB WISE REPORT', txt)
            row = 5
            col = 1
            sheet.set_column(2, 2, 20)
            sheet.set_column(3, 3, 20)
            sheet.set_column(4, 4, 20)
            sheet.set_column(5, 5, 20)
            sheet.set_column(6, 6, 20)
            for class_index, (class_name, students) in enumerate(data['report'].items()):
                row += 1
                sheet.write(row, col + 1, f"Class:{class_name}", cell_format)
                row += 1
                sheet.write(row, col + 1, 'Registration No', txt)
                sheet.write(row, col + 2, 'Name', txt)
                sheet.write(row, col + 3, 'Last Name', txt)
                sheet.write(row, col + 4, 'email', txt)
                row += 1
                for student in students:
                    sheet.write(row, col + 1, f'{student['registration_no']}', txt)
                    sheet.write(row, col + 2, f'{student['name']}', txt)
                    sheet.write(row, col + 3, f'{student['last_name']}', txt)
                    sheet.write(row, col + 4, f'{student['email']}', txt)
                    row += 1
            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()
        else:
            pass

    def cancel(self):
        print('canceled')

