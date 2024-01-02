# Copyright (c) 2023, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    if not filters:
        filters = {}

    if "customer" not in filters:
        filters["customer"] = None

    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = [
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 200
        },
    ]
    return columns

def get_data(filters):
    data = []
    query = """
        SELECT
            cu.name AS customer
        FROM 
            `tabCompliance Agreement` s
        INNER JOIN
            `tabCustomer` cu ON s.customer = cu.name
    """

    if filters.get("customer"):
        query += " WHERE cu.name = '{0}'".format(filters.get("customer"))

    query += " GROUP BY cu.name;"

    # Execute the query and fetch data
    data = frappe.db.sql(query, as_dict=True)

    return data
