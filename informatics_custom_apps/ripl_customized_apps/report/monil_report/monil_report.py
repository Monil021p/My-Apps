# Copyright (c) 2025, Monil Kamboj and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	if filters is None:
		return
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{"label": "Plant", "fieldtype": "Data", "fieldname": "plant"},
		{"label": "Debit", "fieldtype": "Data", "fieldname": "debit"},
		{"label": "Credit", "fieldtype": "Data", "fieldname": "credit"},
		{"label": "GL Entry", "fieldtype": "Link", "fieldname": "gl_entry", "options": "GL Entry"},
		{"label": "Sales Invoice", "fieldtype": "Link", "fieldname": "s_inv", "options": "Sales Invoice"},
		{"label": "Purchase Invoice", "fieldtype": "Link", "fieldname": "p_inv", "options": "Purchase Invoice"},
		{"label": "Cost Center", "fieldtype": "Data", "fieldname": "cost_center"},
		{"label": "Customer Code", "fieldtype": "Link", "fieldname": "customer", "options": "Customer"},
		{"label": "Customer Name", "fieldtype": "Data", "fieldname": "customer_name"},
		{"label": "Supplier Code", "fieldtype": "Link", "fieldname": "supplier", "options": "Supplier"},
		{"label": "Supplier Name", "fieldtype": "Data", "fieldname": "supplier_name"},
		{"label": "Date", "fieldtype": "Date", "fieldname": "posting_date", "read_only": 1},
		{"label": "Segment", "fieldtype": "Data", "fieldname": "segment"},
		{"label": "Item Group", "fieldtype": "Data", "fieldname": "custom_item_group"},
		{"label": "Item Code", "fieldtype": "Link", "fieldname": "item", "options": "Item"},
		{"label": "Item Name", "fieldtype": "Data", "fieldname": "item_name"},
		{"label": "Quantity", "fieldtype": "Data", "fieldname": "qty"},
		{"label": "Rate", "fieldtype": "Data", "fieldname": "rate"},
		{"label": "Amount", "fieldtype": "Data", "fieldname": "amount"},
		{"label": "Total Tax", "fieldtype": "Data", "fieldname": "total_taxes_and_charges"},
		{"label": "Grand Total", "fieldtype": "Data", "fieldname": "grand_total"},
		{"label": "UOM", "fieldtype": "Data", "fieldname": "uom"},
	]

def get_data(filters=None):
	output = []

	# Get Plant and Account
	plant = frappe.get_doc("Branch", filters.get("plant"))
	account = frappe.get_doc("Account", filters.get("account"))

	# Get GL Entries
	gl_entries = frappe.get_all(
    "GL Entry",
    filters={
        "branch": plant.name,
        "docstatus": 1,
        "account": account.name,
        "posting_date": ["between", [filters.get("from_date"), filters.get("to_date")]]
    },
    fields=["name", "voucher_type", "voucher_no"], 
    limit_page_length=10000 
)

	print("--------------------------------------->GL:",gl_entries)
	print("----------------->Number of GL Entries found:", len(gl_entries))
	for gl in gl_entries:
		if gl.voucher_type == "Sales Invoice":
			gle=frappe.get_doc("GL Entry", gl.name)
			sales_invoice = frappe.get_doc("Sales Invoice", gl.voucher_no)
			print("------------------->salesinvoice",sales_invoice)
			for item in sales_invoice.items:
				output.append({
					"plant": plant.name,
					"s_inv": sales_invoice.name,
					"debit": gle.debit,
					"credit":gle.credit,
					"gl_entry":gle.name,
					"cost_center": sales_invoice.cost_center,
					"customer": sales_invoice.customer,
					"customer_name": sales_invoice.customer_name,
					"posting_date": sales_invoice.posting_date,
					"segment": sales_invoice.segment,
					"custom_item_group": sales_invoice.custom_item_group,
					"item": item.item_code,
					"item_name": item.item_name,
					"qty": item.qty,
					"rate": item.rate,
					"amount": item.amount,
					"uom": item.uom,
					"total_taxes_and_charges": sales_invoice.total_taxes_and_charges,
					"grand_total": sales_invoice.grand_total
				})

		elif gl.voucher_type == "Purchase Invoice":
			purchase_invoice = frappe.get_doc("Purchase Invoice", gl.voucher_no)
			gle = frappe.get_doc("GL Entry", gl.name)
			for item in purchase_invoice.items:
				output.append({
					"plant": plant.name,
					"p_inv": purchase_invoice.name,
					"cost_center": purchase_invoice.cost_center,
					"supplier": purchase_invoice.supplier,
					"gl_entry":gle.name,
					"supplier_name": purchase_invoice.supplier_name,
					"posting_date": purchase_invoice.posting_date,
					"segment": purchase_invoice.segment,
					"item": item.item_code,
					"item_name": item.item_name,
					"debit": gle.debit,
					"credit":gle.credit,
					"qty": item.qty,
					"rate": item.rate,
					"amount": item.amount,
					"uom": item.uom,
					"total_taxes_and_charges": purchase_invoice.total_taxes_and_charges,
					"grand_total": purchase_invoice.grand_total
				})

	return output
