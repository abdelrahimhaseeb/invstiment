frappe.pages['workspaces-hub'].on_page_load = function(wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('مساحات العمل'),
		single_column: true
	});

	const $container = $(wrapper).find('.layout-main-section');
	// Hide left workspace sidebar for this page and expand content (multiple selectors for robustness)
	const selectors = ['.layout-side-section', '.side-section', '.desk-sidebar', '.standard-sidebar', '.app-sidebar', '.workspace-sidebar'];
	selectors.forEach(sel => $(wrapper).find(sel).hide());
	$(wrapper).find('.layout-main-section-wrapper').css({flex: '1 1 100%', maxWidth: '100%'});
	$container.empty();
	// Use static HTML structure from .html; just find grid and search
	const $grid = $(wrapper).find('.hub-grid');
	const $search = $(wrapper).find('#hub-search-input');

	// color palette for tiles
	const palette = [
		'#d06e6e','#d08a6e','#d0b16e','#9eb86b','#65b7a6','#6a9fd0','#8a76d0','#b06ecb','#cc6e94','#d0876e'
	];
	const pickColor = (name) => {
		let h = 0; for (let i = 0; i < name.length; i++) h = (h*31 + name.charCodeAt(i)) >>> 0;
		return palette[h % palette.length];
	};

	function add_tile({name,title,icon}){
		const color = pickColor(name);
		const icon_html = icon && (icon.includes(' ') || icon.includes('fa-') || icon.includes('octicon'))
			? `<span class="${icon}" aria-hidden="true"></span>`
			: `<span class="fa fa-${icon||'cubes'}" aria-hidden="true"></span>`;
		const safe_title = frappe.utils.escape_html(title || name);
		const card = $(`
			<div class="hub-card" role="button" style="cursor:pointer;text-align:center;">
				<div class="odoo-circle" style="--tile-bg:${color}">
					<div class="odoo-icon">${icon_html}</div>
				</div>
				<div class="odoo-label">${safe_title}</div>
			</div>
		`);
		card.on('click', () => frappe.set_route('workspace', name));
		$grid.append(card);
	}

	function render_from_pages(pages){
		let count = 0;
		const sorted = [...pages].sort((a,b)=>{
			const sa = a.sequence_id ?? 9999, sb = b.sequence_id ?? 9999;
			if (sa !== sb) return sa - sb;
			const ta = (a.title||a.name||'').toLowerCase();
			const tb = (b.title||b.name||'').toLowerCase();
			return ta.localeCompare(tb);
		});
		const seen = new Set();
		for (const p of sorted) {
			const key = (p.name||'') + '|' + (p.title||'');
			if (seen.has(key)) continue; seen.add(key);
			// Show all allowed pages (public or private), even if marked hidden
			add_tile({name: p.name, title: p.title || p.name, icon: p.icon});
			count++;
		}
		return count;
	}

	function render_from_boot(){
		let count = 0;
		const aw = (frappe.boot && frappe.boot.allowed_workspaces) || [];
		for (const w of aw){
			add_tile({name: w.name, title: w.title || w.name, icon: w.icon});
			count++;
		}
		return count;
	}

	// Fetch allowed workspaces and render tiles; fallback to boot if needed
	frappe.xcall('frappe.desk.desktop.get_workspace_sidebar_items').then(res => {
		const pages = (res && res.pages) || [];
		let shown = render_from_pages(pages);
		if (!shown) {
			shown = render_from_boot();
		}
		if (!shown) {
			// last-resort fallback: fetch Workspace doctype directly
			frappe.xcall('frappe.client.get_list', {
				doctype: 'Workspace',
				fields: ['name','title','icon','public','is_hidden','sequence_id'],
				limit_page_length: 500
			}).then(ws => {
				let c=0;
				const items = (ws||[]).map(w=>({
					name: w.name, title: w.title||w.name, icon: w.icon, sequence_id: w.sequence_id
				}));
				const srt = items.sort((a,b)=>{
					const sa = a.sequence_id ?? 9999, sb = b.sequence_id ?? 9999;
					if (sa !== sb) return sa - sb;
					return (a.title||'').localeCompare(b.title||'');
				});
				srt.forEach(it=>{ add_tile(it); c++; });
				if(!c){
					$grid.append(`<div style=\"grid-column:1/-1;color:#fff;opacity:.9;text-align:center\">${__('لا توجد مساحات عمل متاحة')}</div>`);
				}
			});
		}
		// simple client-side filter
		$search.on('input', function(){
			const q = (this.value||'').trim().toLowerCase();
			$grid.find('.hub-card').each(function(){
				const t = $(this).find('.odoo-label').text().toLowerCase();
				$(this).toggle(t.includes(q));
			});
		});
	});
};

// Toggle a body class when this page is active to hide the desk sidebar via CSS
frappe.pages['workspaces-hub'].on_page_show = function() {
	try {
		document.body.classList.add('hub-active');
		document.body.setAttribute('data-route','app/page/workspaces-hub');
		// double-check hide in case outer containers are outside wrapper
		const hideAll = ['.layout-side-section', '.side-section', '.desk-sidebar', '.standard-sidebar', '.app-sidebar', '.workspace-sidebar'];
		hideAll.forEach(sel => {
			const el = document.querySelector(sel);
			if (el) el.style.setProperty('display','none','important');
		});
		const wrap = document.querySelector('.layout-main-section-wrapper');
		if (wrap) { wrap.style.setProperty('max-width','100%','important'); wrap.style.setProperty('flex','1 1 100%','important'); }
	} catch(e){}
};

frappe.pages['workspaces-hub'].on_page_hide = function() {
	try { document.body.classList.remove('hub-active'); } catch(e){}
};
