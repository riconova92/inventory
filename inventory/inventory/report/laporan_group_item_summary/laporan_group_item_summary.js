// Copyright (c) 2016, Myme and contributors
// For license information, please see license.txt

frappe.query_reports["Laporan Group Item Summary"] = {
	"filters": [
		{
			"fieldname": "item",
			"label":__("Item"),
			"fieldtype": "Link",
			"options": "Item",
			"get_query": function(){ 
				return {
					"filters": [
		                ["stock_uom", "in", ["Yard","Meter"]],
		                ["variant_of", "!=", ""]
		            ]
	        	}
	        }
			
		},
		{
			"fieldname": "show_complete_group",
			"label":__("Show Complete Group"),
			"fieldtype": "Check",
		},

	]
}
