// Copyright (c) 2016, Myme and contributors
// For license information, please see license.txt

frappe.query_reports["Inventory Ledger"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label":__("From"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "to_date",
			"label":__("To"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "type",
			"label":__("Type"),
			"fieldtype": "Select",
			"options": "Sales Order" + '\n'
				+ "Sales Invoice" + '\n'
				+ "Delivery Note" + '\n'
				+ "Stock Entry" + '\n'
				+ "Purchase Order" + '\n'
				+ "Purchase Invoice" + '\n'
				+ "Purchase Receipt"
		}
	]
}
