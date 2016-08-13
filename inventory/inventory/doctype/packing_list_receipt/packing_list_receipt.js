// Copyright (c) 2016, Myme and contributors
// For license information, please see license.txt

frappe.ui.form.on('Packing List Receipt', {
	refresh: function(frm) {

	}
});


cur_frm.cscript.add_item= function(doc,dt,dn) {
	cur_frm.call({
		"method": 'inventory.inventory.doctype.packing_list_receipt.packing_list_receipt.add_item',
		"args": {
			"self": doc
},
	});

}