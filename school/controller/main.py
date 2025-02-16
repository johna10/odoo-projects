import base64
import json
from odoo import http, fields
from odoo.http import content_disposition, request
from odoo.http import serialize_exception as _serialize_exception
from odoo.tools import html_escape

class HttpController(http.Controller):
    """XlsxReport generating controller"""
    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
    def get_report_xlsx(self, model, options, output_format, **kw):
        """
        Generate an XLSX report based on the provided data and return it as a
        response.
        """
        uid = request.session.uid
        report_obj = request.env[model].with_user(uid)
        options = json.loads(options)
        token = 'dummy-because-api-expects-one'
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition',
                         content_disposition('Leave Excel Report' + '.xlsx'))
                    ]
                )
                report_obj.get_xlsx_report(options, response)
                response.set_cookie('fileToken', token)
                return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))

    @http.route('/student/admission', auth='public', website=True)
    def web_form(self):
        """Redirect to the student registration form."""
        classes = request.env['school.class'].sudo().search([])
        clubs = request.env['school.club'].sudo().search([])
        return request.render('school.student_website_data',{'classes':classes, 'clubs':clubs})

    @http.route('/webform/submit', auth='public', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        """Create record in the student.registration model."""
        selected_club_ids = request.httprequest.form.getlist('type')
        clubs_ids = []
        if selected_club_ids:
            clubs_ids = [int(i) for i in selected_club_ids]

        file_name = post.get('tc').filename
        file = post.get('tc')
        attachment_id = request.env['ir.attachment'].create({
            'name': file_name,
            'type': 'binary',
            'datas': base64.b64encode(file.read()),
            'res_model': 'student.registration',
        })
        request.env['student.registration'].sudo().create({
            'name': post.get('name'),
            'last_name': post.get('last_name'),
            'father_name': post.get('father_name'),
            'mother_name': post.get('mother_name'),
            'class_id': post.get('class'),
            'phone': post.get('phone'),
            'email': post.get('email'),
            'date_of_birth': post.get('date_of_birth'),
            'age': post.get('age'),
            'gender': post.get('gender'),
            'aadhaar_number': post.get('aadhaar_number'),
            'tc': [(fields.Command.link(attachment_id.id))],
            'clubs_ids': clubs_ids,
        })
        return request.render('school.thankyou_data')

    @http.route('/email/aadhaar/rpc/check', type='json', auth='public', website=True)
    def email_aadhar_check_rpc_method(self, email, aadhar):
        """Method used for check the entered email, aadhar is already taken or not."""
        email_taken = False
        aadhar_taken = False
        # students_no = request.env['student.registration'].sudo().search_count(['|', ('email', '=', email), ('aadhaar_number', '=', aadhar)])
        # print(students_no)
        students = request.env['student.registration'].sudo().search([])
        existing_emails = students.mapped('email')
        existing_aadhar_number = students.mapped('aadhaar_number')
        if email in existing_emails:
            email_taken = True
        if aadhar in existing_aadhar_number:
            aadhar_taken = True
        return {'email_taken':email_taken , 'aadhar_taken':aadhar_taken}

class SchoolEventsDynamicSnippets(http.Controller):
    """This class is used to pass the values to the dynamic snippets."""
    @http.route(['/total_product_sold'], type="json", auth="public")
    def sold_total(self):
        sale_obj = request.env['sale.order'].sudo().search([
           ('state', 'in', ['done', 'sale']),
        ])
        total_sold = sum(sale_obj.mapped('order_line.product_uom_qty'))
        return total_sold





