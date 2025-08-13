// Add a small Apps Hub button into the toolbar for quick access
(function() {
    frappe.after_ajax(() => {
        try {
            if (frappe.ui?.toolbar?.add_dropdown_button) {
                        frappe.ui.toolbar.add_dropdown_button('Help', __('مساحات العمل'), () => {
                            frappe.set_route('page', 'workspaces-hub');
                }, 'fa fa-th');
            }
            // If still on generic route after 1s, force open hub (one-time)
            setTimeout(() => {
                const r = frappe.get_route();
                const generic = !r[0] || r[0] === 'home' || r[0] === 'modules' || (r[0] === 'workspace' && !r[1]);
                        if (generic && !window.__went_to_hub__) {
                    window.__went_to_hub__ = true;
                            frappe.set_route('page', 'workspaces-hub');
                }
            }, 1000);
        } catch (e) {
            // silent
        }
    });
})();
