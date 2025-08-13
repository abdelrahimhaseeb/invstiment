// Redirect to the Workspaces Hub by default and guard workspace routes
(function () {
        function force_hide_sidebar(){
            try{
                const css = `
                body.no-sidebar .layout-side-section,
                body.no-sidebar .side-section,
                body.no-sidebar .desk-sidebar,
                body.no-sidebar .standard-sidebar,
                body.no-sidebar .app-sidebar,
                body.no-sidebar .workspace-sidebar{display:none!important}
                body.no-sidebar .layout-main-section-wrapper{max-width:100%!important;flex:1 1 100%!important}`;
                if(!document.getElementById('hub-inline-hide-style')){
                    const s=document.createElement('style');
                    s.id='hub-inline-hide-style';
                    s.textContent=css;
                    document.head.appendChild(s);
                }
            }catch(e){}
        }
        function nuke_sidebar_nodes(){
            try{
                const sels = ['.layout-side-section', '.side-section', '.desk-sidebar', '.standard-sidebar', '.app-sidebar', '.workspace-sidebar'];
                document.body.classList.add('no-sidebar');
                sels.forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => {
                        el.style.setProperty('display','none','important');
                        // also remove if inside layout and safe to drop
                        if (el.classList.contains('desk-sidebar') || el.classList.contains('workspace-sidebar')) {
                            try { el.remove(); } catch(e){}
                        }
                    });
                });
            }catch(e){}
        }
        function should_redirect_to_hub(route) {
            const base = route[0];
            // Don't redirect on Home (we render the hub overlay there)
            if (!base || base === 'home') return false;
            // Redirect on first load for any desk route except when already on hub page
            const already_hub = base === 'page' && route[1] === 'workspaces-hub';
            return !already_hub;
        }

        function go_hub_once() {
        if (window.__went_to_hub__) return;
        window.__went_to_hub__ = true;
            frappe.set_route('page', 'workspaces-hub');
    }

    frappe.after_ajax(() => {
        try {
        force_hide_sidebar();
        try { document.body.classList.add('hub-global'); document.body.classList.add('no-sidebar'); } catch(e){}
            // observe DOM to kill any sidebar injected later
            try {
                nuke_sidebar_nodes();
                const obs = new MutationObserver(() => nuke_sidebar_nodes());
                obs.observe(document.body, {childList:true, subtree:true});
            } catch(e){}
            const route = frappe.get_route();
            if (should_redirect_to_hub(route)) {
                go_hub_once();
            }

            // Extra: hard redirect fallbacks after short delays (skip Home so it shows the launcher)
            setTimeout(() => {
                const r1 = frappe.get_route() || [];
                if (!r1[0] || r1[0] === 'modules') {
                    try { frappe.set_route('page','workspaces-hub'); } catch(e){}
                }
            }, 300);
            setTimeout(() => {
                const r2 = frappe.get_route() || [];
                if (!r2[0] || r2[0] === 'modules') {
                    try { window.location.assign('/app/page/workspaces-hub'); } catch(e){}
                }
            }, 900);

            // Guard: if user lands on any workspace route, prefer the hub
                    frappe.router.on('change', () => {
                        const r = frappe.get_route();
                        try { document.body.setAttribute('data-route', r.join('/')); document.body.classList.add('no-sidebar'); force_hide_sidebar(); } catch(e){}
                        try { nuke_sidebar_nodes(); } catch(e){}
                    });
                try { document.body.setAttribute('data-route', route.join('/')); } catch(e){}
        } catch (e) {
            // silent
        }
    });
})();
