// Copyright (c) 2025, Monil Kamboj and contributors
// For license information, please see license.txt

frappe.ui.form.on('Personnel Entry Ledger', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            // Check if the user has the 'Stock User' role
            if (frappe.user.has_role("Stock User")) {
                frm.add_custom_button(__('Return'), function() {
                    let returnable_items = frm.doc.item_details.filter(item => item.balance > 0);
                    
                    if (returnable_items.length === 0) {
                        frappe.msgprint(__('No items available for return.'));
                        return;
                    }
                    
                    const dialog = new frappe.ui.Dialog({
                        title: __('Return Items'),
                        fields: [
                            {
                                fieldtype: 'Table',
                                fieldname: 'return_items',
                                label: __('Return Items'),
                                cannot_add_rows: 1,
                                fields: [
                                    {
                                        fieldtype: 'Data',
                                        fieldname: 'item_name',
                                        label: __('Item Name'),
                                        read_only: 1,
                                        in_list_view: 1
                                    },
                                    {
                                        fieldtype: 'Data',
                                        fieldname: 'balance',
                                        label: __('Balance'),
                                        read_only: 1,
                                        in_list_view: 1
                                    },
                                    {
                                        fieldtype: 'Float',
                                        fieldname: 'returned_quantity',
                                        label: __('Return Quantity'),
                                        reqd: 1,
                                        in_list_view: 1
                                    }
                                ],
                                data: returnable_items.map(item => ({
                                    item_name: item.item_name,
                                    balance: item.balance,
                                    returned_quantity: 0,
                                    item_reference: item
                                })),
                                get_data: function() {
                                    return dialog.fields_dict.return_items.grid.get_data();
                                }
                            }
                        ],
                        primary_action_label: __('Submit'),
                        primary_action: function() {
                            let returned_data = dialog.fields_dict.return_items.grid.get_data();
                            
                            returned_data.forEach(row => {
                                let item = frm.doc.item_details.find(i => i.item_name === row.item_name);
                                if (row.returned_quantity > item.balance || row.returned_quantity < 0) {
                                    frappe.show_alert({
                                        message: __(`Return quantity for ${row.item_name} cannot exceed balance.`),
                                        indicator: "red"
                                    }, 10);
                                    return;
                                } else if (row.returned_quantity <= item.balance && row.returned_quantity > 0) {
                                    item.returned_quantity = (item.returned_quantity || 0) + row.returned_quantity;
                                    item.balance -= row.returned_quantity;
                                    item.return_date = frappe.datetime.nowdate();
                                }
                            });
                            
                            frm.refresh_field('item_details');
                            frm.save('Submit');
                            dialog.hide();
                        }
                    });
                    
                    dialog.show();
                });
            }
        }
    },

    nature: function(frm) {
        frm.set_value('employee', "");
        frm.refresh_field('employee');

        if (frm.doc.nature == "Employee") {
            frm.set_query("employee", function() {
                return {
                    filters: { company: frm.doc.company }
                };
            });
        } else {
            frm.set_query("employee", null);
        }

        frm.set_query("item_code", "item_details", function(doc) {
            return {
                filters: { is_stock_item: 1 }
            };
        });
    },

    before_submit: function(frm) {
        balance_init(frm);
        
        frm.doc.item_details.forEach(function(item) {
            item.issue_date = frappe.datetime.nowdate();
            frm.refresh_field('item_details');
        });
        
        if (frm.doc.owner !== "Administrator") {
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Employee',
                    filters: { 'user_id': frm.doc.owner },
                    fields: ['name', 'employee_name', 'custom_level']
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        frm.set_value("custom_employee", r.message[0].name);
                        frm.refresh_field("custom_employee");
                        frm.set_value("employee_name", r.message[0].employee_name);
                        frm.refresh_field("employee_name");
                    } else {
                        frappe.msgprint(__('No employee record found for the creation user.'));
                    }
                }
            });
        }
    },

    employee: function(frm) {
        frm.clear_table("item_details");
        frm.refresh_field("item_details");
    },

    validate: function(frm) {
        let item_codes = [];
        let duplicate_found = false;

        frm.doc.item_details.forEach(item => {
            if (item_codes.includes(item.item_code)) {
                duplicate_found = true;
                frappe.msgprint(__('Duplicate item_code found: {0}', [item.item_code]));
            }
            item_codes.push(item.item_code);
        });

        if (duplicate_found) {
            frappe.validated = false; // Prevent form submission
        }
    }
});

function balance_init(frm) {
    frm.doc.item_details.forEach((item) => {
        if (item.quantity) {
            item.balance = item.quantity;
        }
    });
}
