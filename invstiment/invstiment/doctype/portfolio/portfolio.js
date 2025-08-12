frappe.ui.form.on('Portfolio', {
	refresh(frm) {
		// Button: View Plans for this Portfolio (opens filtered list)
		frm.add_custom_button(__('الخطط'), () => {
			frappe.set_route('List', 'Portfolio Plan', { portfolio: frm.doc.name });
		}, __('عرض'));

		// Optional quick action: create a new plan pre-filled with this portfolio
		frm.add_custom_button(__('خطة جديدة'), () => {
			frappe.new_doc('Portfolio Plan', { portfolio: frm.doc.name });
		}, __('إنشاء'));
	}
});
