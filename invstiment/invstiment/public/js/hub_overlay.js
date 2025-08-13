// Fullscreen overlay that turns Home into an Odoo-like app launcher
(function(){
  function buildOverlay(){
    let overlay = document.getElementById('hub-overlay');
    if (overlay) return overlay;
    overlay = document.createElement('div');
    overlay.id = 'hub-overlay';
    overlay.style.cssText = 'position:fixed;inset:0;z-index:9999;display:none;overflow:auto;';
    overlay.innerHTML = `
      <div class="workspaces-hub">
        <div class="hub-inner">
          <div class="hub-header">
            <h2>${__('مساحات العمل')}</h2>
            <div class="hub-sub">${__('اختر تطبيقاً للمتابعة')}</div>
          </div>
          <div class="hub-search"><input type="text" placeholder="${__('ابحث عن تطبيق...')}" id="hub-overlay-search" /></div>
          <div class="hub-grid"></div>
        </div>
      </div>`;
    document.body.appendChild(overlay);
    return overlay;
  }

  const palette = ['#d06e6e','#d08a6e','#d0b16e','#9eb86b','#65b7a6','#6a9fd0','#8a76d0','#b06ecb','#cc6e94','#d0876e'];
  function pickColor(name){ let h=0; for(let i=0;i<name.length;i++) h=(h*31+name.charCodeAt(i))>>>0; return palette[h%palette.length]; }

  function addTile(grid, {name,title,icon}){
    const color = pickColor(name||'');
    const icon_html = icon && (icon.includes(' ')||icon.includes('fa-')||icon.includes('octicon'))
      ? `<span class="${icon}" aria-hidden="true"></span>`
      : `<span class="fa fa-${icon||'cubes'}" aria-hidden="true"></span>`;
    const safe_title = frappe.utils.escape_html(title||name);
    const el = document.createElement('div');
    el.className = 'hub-card';
    el.style.cssText='cursor:pointer;text-align:center';
    el.innerHTML = `
      <div class="odoo-circle" style="--tile-bg:${color}">
        <div class="odoo-icon">${icon_html}</div>
      </div>
      <div class="odoo-label">${safe_title}</div>`;
    el.onclick = ()=>{ frappe.set_route('workspace', name) };
    grid.appendChild(el);
  }

  function renderFromPages(grid, pages){
    let count=0;
    const sorted=[...pages].sort((a,b)=>{
      const sa=a.sequence_id??9999, sb=b.sequence_id??9999; if(sa!==sb) return sa-sb;
      return (a.title||a.name||'').localeCompare(b.title||b.name||'');
    });
    const seen=new Set();
    for(const p of sorted){
      const key=(p.name||'')+'|'+(p.title||''); if(seen.has(key)) continue; seen.add(key);
      addTile(grid,{name:p.name,title:p.title||p.name,icon:p.icon}); count++;
    }
    return count;
  }

  function renderFromBoot(grid){
    let count=0; const aw=(frappe.boot&&frappe.boot.allowed_workspaces)||[];
    for(const w of aw){ addTile(grid,{name:w.name,title:w.title||w.name,icon:w.icon}); count++; }
    return count;
  }

  function showOverlay(){
    const ov = buildOverlay();
    const grid = ov.querySelector('.hub-grid');
    const search = ov.querySelector('#hub-overlay-search');
    grid.innerHTML='';
    document.body.classList.add('hub-active','no-sidebar');
    frappe.xcall('frappe.desk.desktop.get_workspace_sidebar_items').then(res=>{
      const pages=(res&&res.pages)||[];
      let shown=renderFromPages(grid,pages);
      if(!shown) shown=renderFromBoot(grid);
      if(!shown){
        frappe.xcall('frappe.client.get_list', { doctype:'Workspace', fields:['name','title','icon','sequence_id'], limit_page_length:500 })
          .then(ws=>{ (ws||[]).forEach(w=>addTile(grid,{name:w.name,title:w.title||w.name,icon:w.icon})); });
      }
      search.addEventListener('input', function(){
        const q=(this.value||'').trim().toLowerCase();
        grid.querySelectorAll('.hub-card').forEach(card=>{
          const t=(card.querySelector('.odoo-label')?.textContent||'').toLowerCase();
          card.style.display = t.includes(q)?'':'none';
        });
      });
      ov.style.display='block';
    });
  }

  function hideOverlay(){
    const ov = document.getElementById('hub-overlay');
    if(ov){ov.style.display='none';}
  }

  frappe.after_ajax(()=>{
    try{
      const route = frappe.get_route();
      const on_home = route[0]==='home';
      if(on_home){ showOverlay(); }
      frappe.router.on('change',()=>{
        const r=frappe.get_route();
        if(r[0]==='home') showOverlay(); else hideOverlay();
      });
    }catch(e){/*no-op*/}
  });
})();
