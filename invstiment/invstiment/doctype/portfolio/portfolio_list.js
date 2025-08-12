frappe.listview_settings['Portfolio'] = {
	button: {
		show: function(doc) {
			return true;
		},
		get_label: function() {
			return __('الخطط');
		},
		get_description: function(doc) {
			return __('عرض الخطط للمحفظة {0}', [doc.name]);
		},
		action: function(doc) {
			frappe.set_route('List', 'Portfolio Plan', { portfolio: doc.name });
		}
	},
	onload(listview) {
		// Open filtered plans when clicking a row (but ignore clicks on checkbox or buttons)
		listview.$result.on('click', '.list-row', function (e) {
			const $target = $(e.target);
			if ($target.closest('.list-row-checkbox, .indicator, .level-item, .btn, .btn-group').length) {
				return; // let default handlers run
			}
			const $row = $(this);
			const nameAttr = $row.attr('data-name') || $row.data('name');
			const data = $row.data('data');
			const docname = nameAttr || (data && data.name);
			if (!docname) return;
			// prevent default navigation to form and open filtered plans instead
			e.preventDefault();
			e.stopPropagation();
			e.stopImmediatePropagation();
			frappe.set_route('List', 'Portfolio Plan', { portfolio: docname });
		});

		listview.page.add_menu_item(__('عرض جميع الخطط'), () => {
			frappe.set_route('List', 'Portfolio Plan');
		});
	}
};
