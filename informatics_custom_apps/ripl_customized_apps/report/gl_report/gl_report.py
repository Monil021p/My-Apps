# Copyright (c) 2025, Monil Kamboj and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date"},
        {"label": "Voucher Type", "fieldname": "voucher_type", "fieldtype": "Data"},
        # {"label": "Voucher No", "fieldname": "voucher_no", "fieldtype": "Link", "options": "GL Entry"},
        
		{"label": "Voucher", "fieldtype": "Dynamic Link", "fieldname": "voucher_no", "options": "voucher_type"},
		{"label": "Voucher Type", "fieldtype": "Data", "fieldname": "voucher_type"},

        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account"},
        {"label": "Party", "fieldname": "party", "fieldtype": "Data"},
        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency"},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency"},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item"},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data"},
        {"label": "Qty", "fieldname": "qty", "fieldtype": "Float"},
        {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency"},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency"},
    ]

def get_data(filters):
    entries = frappe.get_all(
        "GL Entry",
        filters={
            "docstatus": 1,
            "company": filters.get("company"),
            "posting_date": ["between", [filters.get("from_date"), filters.get("to_date")]],
            "account": filters.get("account") if filters.get("account") else ["!=", ""]
        },
        fields=["name", "posting_date", "voucher_type", "voucher_no", "account", "debit", "credit", "party_type", "party"],
        order_by="posting_date asc"
    )

    output = []

    for entry in entries:
        base_row = {
            "posting_date": entry.posting_date,
            "voucher_type": entry.voucher_type,
            "voucher_no": entry.voucher_no,
            "account": entry.account,
            "debit": entry.debit,
            "credit": entry.credit,
            "party": entry.party
        }

        try:
            doc = frappe.get_doc(entry.voucher_type, entry.voucher_no)

            if hasattr(doc, "items"):
                for item in doc.items:
                    row = base_row.copy()
                    row.update({
                        "item_code": item.get("item_code"),
                        "item_name": item.get("item_name"),
                        "qty": item.get("qty"),
                        "rate": item.get("rate"),
                        "amount": item.get("amount")
                    })
                    output.append(row)
            else:
                output.append(base_row)

        except Exception as e:
            frappe.log_error(title="GL Report Error", message=frappe.get_traceback())
            output.append(base_row)

    return output
