# Copyright (c) 2023, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today

def execute(filters=None):
    if not filters:
        filters = {}

    if "compliance_date" not in filters:
        filters["compliance_date"] = today()

    columns = get_columns()
    data = get_data(filters)
    return columns, data, None, None, None

def get_columns():
    columns = [
        {
            "label": _("Compliance Category"),
            "fieldname": "compliance_category",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Compliance Date"),
            "fieldname": "compliance_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Compliance Sub Category"),
            "fieldname": "compliance_sub_category",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 200
        }
    ]
    return columns

def get_data(filters):
    data = []
    query = """
        SELECT
            ca.compliance_category,
            cd.compliance_category,
            cd.compliance_date,
            cd.compliance_sub_category,
            ca.customer
        FROM 
            `tabCompliance Agreement` AS ca
        JOIN
            `tabCompliance Category Details` AS cd
        ON
            ca.compliance_category = cd.compliance_category
        WHERE 
            cd.compliance_date = %(compliance_date)s
    """
    data = frappe.db.sql(query, {"compliance_date": filters["compliance_date"]}, as_dict=1)
    return data
