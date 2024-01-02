// Copyright (c) 2023, efeone and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Compliance Agreement Summary"] = {
	"filters": [
        {
            "label": __("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
        },
	],
};
