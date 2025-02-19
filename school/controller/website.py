import base64
import json
from odoo import http, fields
from odoo.http import content_disposition, request
from odoo.http import serialize_exception as _serialize_exception
from odoo.tools import html_escape

class WebsiteHttpController(http.Controller):
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

    @http.route(['/school/events/'], type="json", auth="public")
    def school_events(self):
        """Method used to fetch the events and return from the school.event model"""
        events = request.env['school.event'].sudo().search([],order="start_date asc", limit=15)
        event_data = [{
            'id': event.id,
            'name': event.name,
            'start_date':event.start_date,
            'venue':event.venue
        } for event in events]
        return event_data

    @http.route(['/event/<int:page>'], type="http", auth="public", website=True)
    def show_individual_event(self, page):
        """Method used to fetch the compete details of a single event clicked."""
        event = request.env['school.event'].browse(page)
        return request.render('school.school_individual_event_template', {'event':event})
