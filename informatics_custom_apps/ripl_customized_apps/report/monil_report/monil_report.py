# Copyright (c) 2025, Monil Kamboj and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	if filters==None:
		return
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return[
		{
			"label":"Plant",
			"fieldtype":"Data",
			"fieldname":"plant",
		},
		{
			"label":"Sales Invoice",
			"fieldtype":"Link",
			"fieldname":"s_inv",
			"options":"Sales Invoice"
		},
		{
			"label":"Purchase Invoice",
			"fieldtype":"Link",
			"fieldname":"p_inv",
			"options":"Purchase Invoice"
		},
		{
			"label":"Cost Center",
			"fieldtype":"Data",
			"fieldname":"cost_center",
		},
		{
			"label":"Customer Code",
			"fieldtype":"Link",
			"fieldname":"customer",
			"options":"Customer"
		},
		{
			"label":"Customer Name",
			"fieldtype":"Data",
			"fieldname":"customer_name",
		},
		{
			"label":"Supplier Code",
			"fieldtype":"Link",
			"fieldname":"supplier",
			"options":"Supplier"
		},
		{
			"label":"Supplier Name",
			"fieldtype":"Data",
			"fieldname":"supplier_name",
		},
		{
			"label":"Date",
			"fieldtype":"Date",
			"fieldname":"posting_date",
			"read_only":1
		},
		{
			"label":"Segment",
			"fieldtype":"Data",
			"fieldname":"segment",
		},
		{
			"label":"Item Group",
			"fieldtype":"Data",
			"fieldname":"custom_item_group",
		},
		{
			"label":"Item Code",
			"fieldtype":"Link",
			"fieldname":"item",
			"options":"Item"
		},
		{
			"label":"Item Name",
			"fieldtype":"Data",
			"fieldname":"item_name",
		},
		{
			"label":"Quantity",
			"fieldtype":"Data",
			"fieldname":"qty",
		},
		{
			"label":"Rate",
			"fieldtype":"Data",
			"fieldname":"rate",
		},
		{
			"label":"Amount",
			"fieldtype":"Data",
			"fieldname":"amount",
		},
		{
			"label":"Total Tax",
			"fieldtype":"Data",
			"fieldname":"total_taxes_and_charges"
		},
		{
			"label":"Grand Total",
			"fieldtype":"Data",
			"fieldname":"grand_total"
		},
		{
			"label":"UOM",
			"fieldtype":"Data",
			"fieldname":"uom",
		}
	]
# def get_data(filters=None):
# 	output=[]
# 	a = frappe.get_doc("Branch",filters.get("plant"))
#   b = frappe.get_all("Sales Invoice",filters={'branch':a.name,'docstatus':1,'posting_date':['BETWEEN',[filters.from_date,filters.to_date]]})
# 	if g.voucher_type == "Sales Invoice":
# 		b = frappe.get_doc("Sales Invoice",{"name":g.voucher_no})
# 		print("------------->Sales Invoice:",b)
# 		for i in b:
# 			sales_invoice = frappe.get_doc("Sales Invoice",i.name)
# 			for item in sales_invoice.items:
# 				item_code=item.item_code
# 				item_name = item.item_name
# 				qty=item.qty
# 				rate=item.rate
# 				amount=item.amount
# 				uom=item.uom
# 			si = {
# 				'plant':a.name,
# 				's_inv':sales_invoice.name,
# 				'cost_center':sales_invoice.cost_center,
# 				'customer':sales_invoice.customer,
# 				'customer_name':sales_invoice.customer_name,
# 				'posting_date':sales_invoice.posting_date,
# 				'segment': sales_invoice.segment,
# 				'custom_item_group': sales_invoice.custom_item_group,
# 				'item': item_code,
# 				'item_name':item_name,
# 				'qty':qty,
# 				'rate':rate,
# 				'amount':amount,
# 				'uom':uom,
# 				'total_taxes_and_charges':sales_invoice.total_taxes_and_charges,
# 				'grand_total':sales_invoice.grand_total
# 			}
# 			print("---------------->",i)
# 			output.append(si)
# 		return output
# 	else:
# 		pass

def get_data(filters=None):
	output=[]
	a = frappe.get_doc("Branch",filters.get("plant"))
	try:
		g = frappe.get_doc("GL Entry",filters.get("gl_entry"))
	except Exception as e:
		print("------Exception:",e)
	# b = frappe.get_all("Sales Invoice",filters={'branch':a.name,'docstatus':1,'posting_date':['BETWEEN',[filters.from_date,filters.to_date]]})
	if g.voucher_type == "Sales Invoice":
		b = frappe.get_doc("Sales Invoice",{"name":g.voucher_no})
		print("------------->Sales Invoice:",b)

		sales_invoice = frappe.get_doc("Sales Invoice",b.name)
		print("------------->Sales Invoice2:",sales_invoice)
		for item in sales_invoice.items:
			item_code=item.item_code
			item_name = item.item_name
			qty=item.qty
			rate=item.rate
			amount=item.amount
			uom=item.uom
		si = {
			'plant':a.name,
			's_inv':sales_invoice.name,
			'cost_center':sales_invoice.cost_center,
			'customer':sales_invoice.customer,
			'customer_name':sales_invoice.customer_name,
			'posting_date':sales_invoice.posting_date,
			'segment': sales_invoice.segment,
			'custom_item_group': sales_invoice.custom_item_group,
			'item': item_code,
			'item_name':item_name,
			'qty':qty,
			'rate':rate,
			'amount':amount,
			'uom':uom,
			'total_taxes_and_charges':sales_invoice.total_taxes_and_charges,
			'grand_total':sales_invoice.grand_total
		}
		# print("---------------->",i)
		output.append(si)
		return output
	elif g.voucher_type == "Purchase Invoice":
		b = frappe.get_doc("Purchase Invoice",{"name":g.voucher_no})
		print("------------->Puhasrcg Invoice:",b)

		purchase_invoice = frappe.get_doc("Purchase Invoice",b.name)
		print("------------->Purchase Invoice2:",purchase_invoice)
		for item in purchase_invoice.items:
			item_code=item.item_code
			item_name = item.item_name
			qty=item.qty
			rate=item.rate
			amount=item.amount
			uom=item.uom
		pi = {
			'plant':a.name,
			'p_inv':purchase_invoice.name,
			'cost_center':purchase_invoice.cost_center,
			'supplier':purchase_invoice.supplier,
			'supplier_name':purchase_invoice.supplier_name,
			'posting_date':purchase_invoice.posting_date,
			'segment': purchase_invoice.segment,
			'item': item_code,
			'item_name':item_name,
			'qty':qty,
			'rate':rate,
			'amount':amount,
			'uom':uom,
			'total_taxes_and_charges':purchase_invoice.total_taxes_and_charges,
			'grand_total':purchase_invoice.grand_total
		}
		# print("---------------->",i)
		output.append(pi)
		return output
	
# @frappe.whitelist()
# def get_report_field_options():
#     field_sources = {
#         "Sales Invoice": "Sales Invoice",
#         "Purchase Invoice": "Purchase Invoice",
#         "Sales Invoice Item": "Sales Invoice Item",
#         "Purchase Invoice Item": "Purchase Invoice Item"
#     }

#     options = []

#     for doctype_label, doctype in field_sources.items():
#         meta = frappe.get_meta(doctype)
#         for df in meta.fields:
#             if df.fieldtype not in ["Section Break", "Column Break", "Button", "HTML"] and df.fieldname:
#                 label = f"{doctype_label} → {df.label or df.fieldname}"
#                 options.append({
#                     "value": f"{doctype}.{df.fieldname}",  # used internally
#                     "label": label  # shown to user
#                 })
	
#     return sorted(options, key=lambda x: x["label"])

# def get_columns(extra_fields=None):
#     base_columns = [
#         {"label": "Plant", "fieldtype": "Data", "fieldname": "plant"},
#         {"label": "Sales Invoice", "fieldtype": "Link", "fieldname": "s_inv", "options": "Sales Invoice"},
#         {"label": "Purchase Invoice", "fieldtype": "Link", "fieldname": "p_inv", "options": "Purchase Invoice"},
#         {"label": "Cost Center", "fieldtype": "Data", "fieldname": "cost_center"},
#         {"label": "Customer Code", "fieldtype": "Link", "fieldname": "customer", "options": "Customer"},
#         {"label": "Customer Name", "fieldtype": "Data", "fieldname": "customer_name"},
#         {"label": "Supplier Code", "fieldtype": "Link", "fieldname": "supplier", "options": "Supplier"},
#         {"label": "Supplier Name", "fieldtype": "Data", "fieldname": "supplier_name"},
#         {"label": "Date", "fieldtype": "Date", "fieldname": "posting_date", "read_only": 1},
#         {"label": "Segment", "fieldtype": "Data", "fieldname": "segment"},
#         {"label": "Item Group", "fieldtype": "Data", "fieldname": "custom_item_group"},
#         {"label": "Item Code", "fieldtype": "Link", "fieldname": "item", "options": "Item"},
#         {"label": "Item Name", "fieldtype": "Data", "fieldname": "item_name"},
#         {"label": "Quantity", "fieldtype": "Data", "fieldname": "qty"},
#         {"label": "Rate", "fieldtype": "Data", "fieldname": "rate"},
#         {"label": "Amount", "fieldtype": "Data", "fieldname": "amount"},
#         {"label": "Total Tax", "fieldtype": "Data", "fieldname": "total_taxes_and_charges"},
#         {"label": "Grand Total", "fieldtype": "Data", "fieldname": "grand_total"},
#         {"label": "UOM", "fieldtype": "Data", "fieldname": "uom"},
#     ]

#     dynamic_columns = []
#     for field in extra_fields or []:
#         doctype, fieldname = field.split(".", 1)
#         meta = frappe.get_meta(doctype)
#         df = next((f for f in meta.fields if f.fieldname == fieldname), None)
#         if df:
#             dynamic_columns.append({
#                 "label": f"{doctype} - {df.label or fieldname}",
#                 "fieldname": field.replace(".", "_"),  # e.g. Sales Invoice.customer_name → sales_invoice_customer_name
#                 "fieldtype": df.fieldtype or "Data",
#             })

#     return base_columns + dynamic_columns
