# Copyright 2025 Miquel Pascual López(APSL-Nagarro)<mpascual@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "HR Timesheet Type Non Billable",
    "version": "18.0.1.0.0",
    "summary": "Configure timesheet types that are not billable to clients and won't affect project remaining time computation.",
    "category": "Timesheet",
    "website": "https://github.com/OCA/timesheet",
    "author": "APSL-Nagarro, Odoo Community Association (OCA)",
    "maintainers": ["mpascuall"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "hr_timesheet",
        "hr_timesheet_time_type",
        "sale_timesheet_line_exclude",
    ],
    "data": [
        "views/project_time_type_view.xml",
    ],
}
