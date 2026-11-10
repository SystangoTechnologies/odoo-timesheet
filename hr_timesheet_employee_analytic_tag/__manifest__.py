# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Hr Timesheet Employee Analytic Tag",
    "version": "18.0.1.0.0",
    "summary": "This module allows to define analytical labels in employees to be set when creating analytical items.",
    "category": "Timesheet",
    "website": "https://github.com/OCA/timesheet",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["hr_timesheet", "account_analytic_tag"],
    "installable": True,
    "data": [
        "views/hr_employee_view.xml",
    ],
    "maintainers": ["victoralmau"],
}
