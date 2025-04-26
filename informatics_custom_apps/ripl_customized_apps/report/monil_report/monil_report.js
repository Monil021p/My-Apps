// Copyright (c) 2025, Monil Kamboj and contributors
// For license information, please see license.txt

frappe.query_reports["Monil Report"] = {
	"filters": [
		{
			fieldname:"plant",
			label: "Plant",
			fieldtype: "Link",
			options:"Branch",
			reqd: 1		
		},
		{
			fieldname:"from_date",
			label: "From Date",
			fieldtype: "Date",
			reqd: 1	
		},
		{
			fieldname:"to_date",
			label: "To Date",
			fieldtype: "Date",
			reqd: 1	
		},
		{
			fieldname:"sales_checkbox",
			label: "Sales",
			fieldtype: "Check",
			reqd: 0	
		}
	]
};
