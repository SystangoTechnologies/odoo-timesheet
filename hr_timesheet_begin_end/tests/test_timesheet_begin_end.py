# Copyright 2015 Camptocamp SA - Guewen Baconnier
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import exceptions, fields
from odoo.tests import Form, common


class TestBeginEnd(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.timesheet_line_model = cls.env["account.analytic.line"]
        cls.analytic = cls.env.ref("analytic.analytic_administratif")
        cls.user = cls.env.ref("base.user_root")
        cls.project = cls.env.ref("project.project_project_1")
        cls.employee = cls.env.ref("hr.employee_admin")
        cls.base_line = {
            "name": "test",
            "date": fields.Date.today(),
            "time_start": 10.0,
            "time_stop": 12.0,
            "user_id": cls.user.id,
            "unit_amount": 2.0,
            "account_id": cls.analytic.id,
            "amount": -60.0,
        }

    def test_onchange(self):
        line = self.timesheet_line_model.new(
            {"name": "test", "time_start": 10.0, "time_stop": 12.0}
        )
        line.onchange_hours_start_stop()
        self.assertEqual(line.unit_amount, 2)

    def test_onchange_no_update(self):
        line = self.timesheet_line_model.new(
            {"name": "test", "time_start": 13.0, "time_stop": 12.0}
        )
        line.onchange_hours_start_stop()
        self.assertEqual(line.unit_amount, 0)

    def test_check_valid_working_interval(self):
        """TS-01: a normal 09:00-17:00 interval must save."""
        line = self.base_line.copy()
        line.update({"time_start": 9.0, "time_stop": 17.0, "unit_amount": 8.0})
        record = self.timesheet_line_model.create(line)
        self.assertEqual(record.time_start, 9.0)
        self.assertEqual(record.time_stop, 17.0)
        self.assertEqual(record.unit_amount, 8.0)

    def test_form_save_valid_working_interval(self):
        """TS-01 UI: form onchange + save accepts 09:00-17:00."""
        hour_uom = self.env.ref("uom.product_uom_hour")
        with Form(
            self.timesheet_line_model.with_context(
                default_product_uom_id=hour_uom.id,
                default_project_id=self.project.id,
                default_employee_id=self.employee.id,
            ),
            view=self.env.ref("hr_timesheet_begin_end.hr_timesheet_line_form"),
        ) as form:
            form.name = "TS-01 UI test"
            form.date = fields.Date.today()
            form.time_start = 9.0
            form.time_stop = 17.0
            self.assertEqual(form.unit_amount, 8.0)
            record = form.save()
        self.assertEqual(record.time_start, 9.0)
        self.assertEqual(record.time_stop, 17.0)
        self.assertEqual(record.unit_amount, 8.0)

    def test_form_rejects_end_before_begin(self):
        """TS-01 UI: form save rejects an end hour before the begin hour."""
        hour_uom = self.env.ref("uom.product_uom_hour")
        with self.assertRaises(exceptions.ValidationError):
            with Form(
                self.timesheet_line_model.with_context(
                    default_product_uom_id=hour_uom.id,
                    default_project_id=self.project.id,
                    default_employee_id=self.employee.id,
                ),
                view=self.env.ref("hr_timesheet_begin_end.hr_timesheet_line_form"),
            ) as form:
                form.name = "TS-01 invalid interval"
                form.date = fields.Date.today()
                form.time_start = 12.0
                form.time_stop = 8.0

    def test_check_begin_before_end(self):
        line = self.base_line.copy()
        line.update({"time_start": 12.0, "time_stop": 10.0})
        with self.assertRaises(exceptions.ValidationError):
            self.timesheet_line_model.create(line)

    def test_check_wrong_duration(self):
        message_re = (
            r"The duration \(\d\d:\d\d\) must be equal to the "
            r"difference between the hours \(\d\d:\d\d\)\."
        )
        line = self.base_line.copy()
        line.update({"time_start": 10.0, "time_stop": 12.0, "unit_amount": 5.0})
        with self.assertRaisesRegex(exceptions.ValidationError, message_re):
            self.timesheet_line_model.create(line)

    def test_check_overlap(self):
        line1 = self.base_line.copy()
        line1.update({"time_start": 10.0, "time_stop": 12.0, "unit_amount": 2.0})
        line2 = self.base_line.copy()
        line2.update({"time_start": 12.0, "time_stop": 14.0, "unit_amount": 2.0})
        self.timesheet_line_model.create(line1)
        self.timesheet_line_model.create(line2)

        message_re = r"overlap"

        line3 = self.base_line.copy()

        line3.update({"time_start": 9.0, "time_stop": 11, "unit_amount": 2.0})
        with self.assertRaisesRegex(exceptions.ValidationError, message_re):
            self.timesheet_line_model.create(line3)

        line3.update({"time_start": 13.0, "time_stop": 15, "unit_amount": 2.0})
        with self.assertRaisesRegex(exceptions.ValidationError, message_re):
            self.timesheet_line_model.create(line3)

        line3.update({"time_start": 8.0, "time_stop": 15, "unit_amount": 7.0})
        with self.assertRaisesRegex(exceptions.ValidationError, message_re):
            self.timesheet_line_model.create(line3)

    def test_check_precision(self):
        line1 = self.base_line.copy()
        line1.update({"time_start": 19.0, "time_stop": 20.314, "unit_amount": 1.314})
        self.timesheet_line_model.create(line1)
