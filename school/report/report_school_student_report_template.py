from odoo import models,api


class ReportSchoolStudentReportTemplate(models.AbstractModel):
    _name = 'report.school.student_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Method used for execute queries based on the wizard data and return to the template."""

        if data['report_type'] == 'class':
            query = """SELECT sr.registration_no, sr.name, sr.last_name , sr.email,
                                sc.name as class_name
                                FROM student_registration sr
                                    INNER JOIN school_class sc ON sc.id = sr.class_id
                                    """
            if data['selected_class_ids']:
                query += """where sc.id in %s order by sc.id"""
                params = [tuple(data['selected_class_ids'])]
                self.env.cr.execute(query, params)
                report_data = self.env.cr.dictfetchall()

                class_wise_report ={}
                for student in report_data:
                    class_name = student.pop('class_name')
                    if class_name not in class_wise_report:
                        class_wise_report[class_name]=[]
                    class_wise_report[class_name].append(student)
            else:                                                   #If no class is selected
                query+="""order by sc.id"""
                self.env.cr.execute(query)
                report_data = self.env.cr.dictfetchall()

                class_wise_report = {}
                for student in report_data:
                    class_name = student.pop('class_name')
                    if class_name not in class_wise_report:
                        class_wise_report[class_name] = []
                    class_wise_report[class_name].append(student)

            data = {
                    'report_type':'Class Wise Report',
                    'report': class_wise_report
                    }

        elif data['report_type'] == 'department':
            query = """SELECT sr.registration_no, sr.name, sr.last_name, sr.email,
                            sc.name as class_name,
                            sd.name as department_name
                        FROM student_registration sr
                            INNER JOIN school_class sc ON sc.id = sr.class_id
                            INNER JOIN school_department sd ON sd.id = sc.department_id"""
            if data['selected_department_ids']:
                query += """ where sd.id in %s order by sd.id"""
                params = [tuple(data['selected_department_ids'])]
                self.env.cr.execute(query, params)
                report_data = self.env.cr.dictfetchall()

                department_wise_report = {}
                for student in report_data:
                    department_name = student.pop('department_name')
                    if department_name not in department_wise_report:
                        department_wise_report[department_name] = []
                    department_wise_report[department_name].append(student)
            else:
                query += """ order by sd.id"""
                self.env.cr.execute(query)
                report_data = self.env.cr.dictfetchall()

                department_wise_report = {}
                for student in report_data:
                    department_name = student.pop('department_name')
                    if department_name not in department_wise_report:
                        department_wise_report[department_name] = []
                    department_wise_report[department_name].append(student)

            data = {
                'report_type': 'Department Wise Report',
                'report': department_wise_report
            }

        elif data['report_type'] == 'club':
            query = """SELECT sr.registration_no, sr.name, sr.last_name, sr.email,
                        sc.name as class_name,
                        sd.name as department_name,
                        scl.name as club_name
                        FROM student_registration sr
                        INNER JOIN school_class sc ON sc.id = sr.class_id
                        INNER JOIN school_department sd ON sd.id = sc.department_id
                        INNER JOIN school_club_student_registration_rel scs ON scs.student_registration_id = sr.id
                        INNER JOIN school_club scl ON scl.id = scs.school_club_id"""
            if data['selected_clubs_ids']:
                query += """ where scl.id in %s"""
                params = [tuple(data['selected_clubs_ids'])]
                self.env.cr.execute(query, params)
                report_data = self.env.cr.dictfetchall()

                club_wise_report = {}
                for student in report_data:
                    club_name = student.pop('club_name')
                    if club_name not in club_wise_report:
                        club_wise_report[club_name] = []
                    club_wise_report[club_name].append(student)
            else:
                query += """ order by scl.id"""
                self.env.cr.execute(query)
                report_data = self.env.cr.dictfetchall()

                club_wise_report = {}
                for student in report_data:
                    club_name = student.pop('club_name')
                    if club_name not in club_wise_report:
                        club_wise_report[club_name] = []
                    club_wise_report[club_name].append(student)
            data = {
                'report_type': 'Club Wise Report',
                'report': club_wise_report
            }
        else:
            pass
        print(data)
        print('this is for student-----------------------------------------------------------------------------------')
        return data
