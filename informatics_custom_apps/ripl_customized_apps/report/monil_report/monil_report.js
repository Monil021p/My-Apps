// Copyright (c) 2025, Monil Kamboj and contributors
// For license information, please see license.txt

// frappe.query_reports["Monil Report"] = {
// 	"filters": [
// 		{
// 			fieldname: "plant",
// 			label: "Plant",
// 			fieldtype: "Link",
// 			options: "Branch",
// 			reqd: 1
// 		},
// 		{
// 			fieldname: "from_date",
// 			label: "From Date",
// 			fieldtype: "Date",
// 			reqd: 1
// 		},
// 		{
// 			fieldname: "to_date",
// 			label: "To Date",
// 			fieldtype: "Date",
// 			reqd: 1
// 		},
// 		{
// 			fieldname: "gl_entry",
// 			label: "GL Entry",
// 			fieldtype: "Link",
// 			options: "GL Entry",
// 			reqd: 1,
// 			get_query: function (doc) {
// 				const plant = frappe.query_report.get_filter_value("plant");
// 				const from_date = frappe.query_report.get_filter_value("from_date");
// 				const to_date = frappe.query_report.get_filter_value("to_date");
		
// 				return {
// 					filters: [
// 						["GL Entry", "branch", "=", plant],
// 						["GL Entry", "posting_date", ">=", from_date],
// 						["GL Entry", "posting_date", "<=", to_date],
// 						["GL Entry", "voucher_type", "IN",["Sales Invoice","Purchase Invoice"]	]
// 					]
// 				};
// 			}
// 		}
		
// 	]
// };

frappe.query_reports["Monil Report"] = {
    "filters": [
        {
            fieldname: "plant",
            label: "Plant",
            fieldtype: "Link",
            options: "Branch",
            reqd: 1
        },
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "gl_entry",
            label: "GL Entry",
            fieldtype: "Link",
            options: "GL Entry",
            reqd: 1,
            get_query: function (doc) {
                const plant = frappe.query_report.get_filter_value("plant");
                const from_date = frappe.query_report.get_filter_value("from_date");
                const to_date = frappe.query_report.get_filter_value("to_date");
        
                return {
                    filters: [
                        ["GL Entry", "branch", "=", plant],
                        ["GL Entry", "posting_date", ">=", from_date],
                        ["GL Entry", "posting_date", "<=", to_date],
                        ["GL Entry", "voucher_type", "IN",["Sales Invoice","Purchase Invoice"]	]
                    ]
                };
            }
        }
        // {
        //     fieldname: "extra_field",
        //     label: "Pick Additional Fields",
        //     fieldtype: "Select",
        //     options: [],  // filled dynamically
        //     reqd: 0
        // }        
    ]
//     onload: function(report) {
//         frappe.call({
//             method: "informatics_custom_apps.ripl_customized_apps.report.monil_report.monil_report.get_report_field_options",
//             callback: function(r) {
//                 if (r.message) {
//                     frappe.show_alert({
//                         message: __('Fields Fetched Successfully!'),
//                         indicator: 'blue'
//                     });
    
//                     let opts = [{ label: "", value: "" }];
//                     (r.message || []).forEach(f => {
//                         opts.push({
//                             label: f.label,
//                             value: f.value
//                         });
//                     });
    
//                     const extraField = frappe.query_report.get_filter("extra_field");
//                     extraField.df.options = opts;
//                     extraField.refresh();
//                 }
//             }
//         });
//     }
    
    
};
