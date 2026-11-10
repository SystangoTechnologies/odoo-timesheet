{
    "name": "HR Timesheet Sheet Attendance",
    "version": "18.0.1.0.3",
    "summary": "This module extends the functionality of hr_timesheet_sheet and helps employees to manage their attendance according to timesheet period.",
    "category": "Human Resources",
    "sequence": 80,
    "license": "AGPL-3",
    "author": "BizzAppDev, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/timesheet",
    "depends": ["hr_attendance", "hr_timesheet_sheet"],
    "data": [
        "views/hr_timesheet_sheet_view.xml",
        "views/hr_attendance_view.xml",
    ],
    "installable": True,
}
