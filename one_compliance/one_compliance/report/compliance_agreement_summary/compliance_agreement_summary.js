// Copyright (c) 2023, efeone and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Compliance Agreement Summary"] = {
	"filters": [
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
	]
};
