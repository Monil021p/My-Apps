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
def get_data(filters=None):
	if filters.sales_checkbox:
		output=[]
		a = frappe.get_doc("Branch",filters.get("plant"))
		b = frappe.get_all("Sales Invoice",filters={'branch':a.name,'docstatus':1,'posting_date':['BETWEEN',[filters.from_date,filters.to_date]]})

		for i in b:
			sales_invoice = frappe.get_doc("Sales Invoice",i.name)
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
			print("---------------->",i)
			output.append(si)
		return output