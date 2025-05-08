// Copyright (c) 2025, Monil Kamboj and contributors
// For license information, please see license.txt
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
            fieldname: "account",
            label: "Account",
            fieldtype: "Link",
            reqd: 1,
            options: "Account"
        }
    ],

    // onload: function(report) {
    //     // Wait for filters to fully render before clearing
    //     setTimeout(() => {
    //         ["plant", "from_date", "to_date", "account"].forEach(fieldname => {
    //             let filter = frappe.query_report.get_filter(fieldname);
    //             if (filter) {
    //                 filter.set_value("");  // or `null`, but "" works better for Link fields
    //             }
    //         });
    //     }, 100);
    // }
    
};
