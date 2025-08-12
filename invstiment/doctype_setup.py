import frappe


def create_study_doctype():
    """Create standard DocType 'Study' under module 'Invstiment'."""
    frappe.only_for("System Manager")

    # Ensure Module Def exists
    if not frappe.db.exists("Module Def", {"module_name": "Invstiment"}):
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": "Invstiment",
            "app_name": "invstiment",
            "custom": 0,
        }).insert(ignore_if_duplicate=True)

    # If DocType already exists, return
    if frappe.db.exists("DocType", "Study"):
        return "DocType 'Study' already exists."

    # Define the DocType
    dt = frappe.get_doc({
        "doctype": "DocType",
        "name": "Study",
        "module": "Invstiment",
        "custom": 0,
        "istable": 0,
        "editable_grid": 0,
        "track_changes": 1,
        "allow_import": 1,
        "fields": [
            {
                "fieldname": "study_name",
                "label": "Study Name",
                "fieldtype": "Data",
                "reqd": 1,
                "in_list_view": 1,
                "in_standard_filter": 1,
            },
            {
                "fieldname": "stage",
                "label": "المرحلة",
                "fieldtype": "Select",
                "options": "مرحلة التنقيب\nالدراسة المبدئية\nالدراسة النهائية",
                "default": "مرحلة التنقيب",
                "in_list_view": 1,
                "in_standard_filter": 1,
            },
            {
                "fieldname": "description",
                "label": "Description",
                "fieldtype": "Small Text",
            },
        ],
        "permissions": [
            {
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
            }
        ],
        "autoname": "STUDY-.#####",
    })

    dt.insert(ignore_if_duplicate=True)
    return "DocType 'Study' created."


def create_sample_study():
    """Insert a sample Study record and return its name."""
    frappe.only_for("System Manager")
    if not frappe.db.exists("DocType", "Study"):
        return "DocType 'Study' not found."

    doc = frappe.get_doc({
        "doctype": "Study",
        "study_name": "Sample Study",
        "stage": "مرحلة التنقيب",
        "description": "Created via bench execute for verification.",
    }).insert(ignore_permissions=True)
    return doc.name


def create_sample_portfolio():
    frappe.only_for("System Manager")
    if not frappe.db.exists("DocType", "Portfolio"):
        return "DocType 'Portfolio' not found."

    p = frappe.get_doc({
        "doctype": "Portfolio",
        "portfolio_name": "محفظة الأسهم السعودية",
        "currency": "SAR",
    }).insert(ignore_permissions=True)
    return p.name


def create_sample_deposit(portfolio_name: str, amount: float = 100000.0):
    frappe.only_for("System Manager")
    if not frappe.db.exists("Portfolio", portfolio_name):
        return "Portfolio not found"

    pcm = frappe.get_doc({
        "doctype": "Portfolio Cash Movement",
        "portfolio": portfolio_name,
        "movement_type": "إيداع",
        "amount": amount,
    }).insert(ignore_permissions=True)
    pcm.submit()
    return pcm.name


def create_sample_plan(portfolio_name: str):
    frappe.only_for("System Manager")
    plan = frappe.get_doc({
        "doctype": "Portfolio Plan",
        "portfolio": portfolio_name,
        "symbol": "TADAWUL:XYZ",
        "fair_value": 90,
        "lowest_price": 70,
        "investment_amount": 50000,
        "division_factor": 20,
    }).insert(ignore_permissions=True)

    # trigger level generation
    from invstiment.invstiment.doctype.portfolio_plan.portfolio_plan import calculate_theoretical_levels
    calculate_theoretical_levels(plan)
    plan.save()
    plan.submit()
    return plan.name


def create_sample_trade(portfolio_name: str, plan_name: str):
    frappe.only_for("System Manager")
    tr = frappe.get_doc({
        "doctype": "Portfolio Trade",
        "portfolio": portfolio_name,
        "plan": plan_name,
        "trade_type": "شراء",
        "qty": 100,
        "price": 85,
    }).insert(ignore_permissions=True)
    tr.submit()
    return tr.name


def create_investment_workspace():
    """Create or update the 'الاستثمار' Workspace so it appears in the Desk sidebar."""
    frappe.only_for("System Manager")

    # Ensure Module Def exists for 'Invstiment'
    if not frappe.db.exists("Module Def", {"module_name": "Invstiment"}):
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": "Invstiment",
            "app_name": "invstiment",
            "custom": 0,
        }).insert(ignore_if_duplicate=True)

    content = (
        "[\n"
        "    {\"id\": \"hdr1\", \"type\": \"header\", \"data\": {\"text\": \"<span class=\\\"h4\\\"><b>المحافظ والاستثمار</b></span>\", \"col\": 12}},\n"
        "    {\"id\": \"sp1\", \"type\": \"spacer\", \"data\": {\"col\": 12}}\n"
        "]"
    )

    data = {
        "doctype": "Workspace",
        # Don't set name explicitly; it will be derived from label by naming rule
        "label": "الاستثمار",
        "title": "الاستثمار",
        # keep module/icon/sequence_id unset to avoid read-only validation issues
        "public": 1,
        "is_hidden": 0,
        "content": content,
        "shortcuts": [
            {"label": "المحافظ", "link_to": "Portfolio", "type": "DocType"},
            {"label": "الخطط", "link_to": "Portfolio Plan", "type": "DocType"},
            {"label": "الصفقات", "link_to": "Portfolio Trade", "type": "DocType"},
            {"label": "حركات نقدية", "link_to": "Portfolio Cash Movement", "type": "DocType"},
        ],
        # Use valid link types; remove unsupported 'Route'
        "links": [
            {"label": "محافظ الاستثمار", "type": "Link", "link_type": "DocType", "link_to": "Portfolio", "hidden": 0, "onboard": 0},
            {"label": "خطط الاستثمار", "type": "Link", "link_type": "DocType", "link_to": "Portfolio Plan", "hidden": 0, "onboard": 0},
            {"label": "صفقات الاستثمار", "type": "Link", "link_type": "DocType", "link_to": "Portfolio Trade", "hidden": 0, "onboard": 0},
            {"label": "حركات نقدية", "type": "Link", "link_type": "DocType", "link_to": "Portfolio Cash Movement", "hidden": 0, "onboard": 0},
        ],
        "charts": [],
        "number_cards": [],
        "quick_lists": [],
        "roles": [],
    }

    # Try locating existing workspace by common identifiers
    existing_name = None
    # by exact name 'investment'
    if frappe.db.exists("Workspace", "investment"):
        existing_name = "investment"
    else:
        # by label/title match
        recs = frappe.get_all("Workspace", filters={"label": data["label"], "public": 1}, pluck="name")
        if recs:
            existing_name = recs[0]

    if existing_name:
        doc = frappe.get_doc("Workspace", existing_name)
        for k, v in data.items():
            if k in ("doctype", "name"):
                continue
            setattr(doc, k, v)
        doc.save(ignore_permissions=True)
        action = "updated"
    else:
        doc = frappe.get_doc(data)
        doc.insert(ignore_permissions=True)
        action = "created"

    # Clear caches so the sidebar refreshes
    frappe.clear_cache()
    try:
        # Invalidate bootinfo and sidebar via known keys when possible
        frappe.cache().delete_key("bootinfo")
    except Exception:
        pass

    return f"Workspace '{doc.name}' {action}."


def _upsert_number_card(label: str,
                        doctype: str,
                        function: str = "Count",
                        aggregate_on: str | None = None,
                        filters: dict | None = None) -> str:
    """Create or update a Number Card and return its name (label)."""
    nc_name = label
    exists = frappe.db.exists("Number Card", nc_name)
    data = {
        "doctype": "Number Card",
        "label": nc_name,
        "type": "Document Type",
        "document_type": doctype,
        "function": function,
        "is_public": 1,
    }
    if function != "Count" and aggregate_on:
        data["aggregate_function_based_on"] = aggregate_on
    if filters:
        data["filters_json"] = frappe.as_json(filters)

    if exists:
        doc = frappe.get_doc("Number Card", nc_name)
        for k, v in data.items():
            setattr(doc, k, v)
        doc.save(ignore_permissions=True)
    else:
        doc = frappe.get_doc(data)
        doc.insert(ignore_permissions=True)
    return nc_name


def enhance_investment_workspace():
    """Wire full Portfolio Management into the الاستثمار workspace: shortcuts, links, KPIs, quick lists."""
    frappe.only_for("System Manager")

    # Get or create base workspace
    ws_name = frappe.get_all("Workspace", filters={"label": "الاستثمار", "public": 1}, pluck="name")
    if not ws_name:
        create_investment_workspace()
        ws_name = frappe.get_all("Workspace", filters={"label": "الاستثمار", "public": 1}, pluck="name")
    if not ws_name:
        return "Workspace 'الاستثمار' not found/created."
    ws_name = ws_name[0]

    ws = frappe.get_doc("Workspace", ws_name)

    # Shortcuts: ensure DocType shortcuts and overview URL
    desired_shortcuts = [
        {"type": "DocType", "link_to": "Portfolio", "label": "المحافظ"},
        {"type": "DocType", "link_to": "Portfolio Plan", "label": "الخطط"},
        {"type": "DocType", "link_to": "Portfolio Trade", "label": "الصفقات"},
        {"type": "DocType", "link_to": "Portfolio Cash Movement", "label": "حركات نقدية"},
        {"type": "URL", "url": "/portfolios", "label": "نظرة عامة على المحافظ"},
    ]
    # remove dups by label
    existing_labels = {s.label for s in ws.shortcuts}
    for sc in desired_shortcuts:
        if sc["label"] in existing_labels:
            continue
        ws.append("shortcuts", sc)

    # Links card
    # Build a single card "الإدارة" with DocType links
    has_admin_card = any(l.type == "Card Break" and l.label == "الإدارة" for l in ws.links)
    if not has_admin_card:
        ws.append("links", {
            "label": "الإدارة",
            "type": "Card Break",
            "icon": None,
            "hidden": 0,
            "link_count": 0,
        })
        for lbl, dt in (
            ("محافظ الاستثمار", "Portfolio"),
            ("خطط الاستثمار", "Portfolio Plan"),
            ("صفقات الاستثمار", "Portfolio Trade"),
            ("حركات نقدية", "Portfolio Cash Movement"),
        ):
            ws.append("links", {
                "label": lbl,
                "type": "Link",
                "link_type": "DocType",
                "link_to": dt,
                "hidden": 0,
                "onboard": 0,
            })

    # KPIs: Number Cards
    nc1 = _upsert_number_card("الاستثمار - عدد المحافظ", "Portfolio", "Count")
    nc2 = _upsert_number_card("الاستثمار - إجمالي الإيداعات", "Portfolio Cash Movement", "Sum", "amount", {"movement_type": "إيداع"})
    nc3 = _upsert_number_card("الاستثمار - إجمالي السحوبات", "Portfolio Cash Movement", "Sum", "amount", {"movement_type": "سحب"})
    nc4 = _upsert_number_card("الاستثمار - عدد الصفقات", "Portfolio Trade", "Count")

    existing_nc = {nc.number_card_name for nc in ws.number_cards}
    for nc in (nc1, nc2, nc3, nc4):
        if nc not in existing_nc:
            ws.append("number_cards", {"number_card_name": nc, "label": nc})

    # Quick lists: latest trades
    if not any(q.document_type == "Portfolio Trade" for q in ws.quick_lists):
        ws.append("quick_lists", {
            "document_type": "Portfolio Trade",
            "label": "أحدث الصفقات",
            # leave filter empty to show recent items
        })

    ws.save(ignore_permissions=True)

    # Clear cache so changes reflect in sidebar
    frappe.clear_cache()
    try:
        frappe.cache().delete_key("bootinfo")
    except Exception:
        pass

    return f"Workspace '{ws.name}' enhanced."


def debug_list_public_workspaces():
    """Return a summary of public workspaces (label, module, is_hidden, sequence_id)."""
    rows = frappe.get_all(
        "Workspace",
        filters={"public": 1},
        fields=["name", "label", "title", "module", "is_hidden", "sequence_id"],
        order_by="sequence_id asc, creation asc",
    )
    return rows


def fix_investment_workspace_module():
    """Ensure the 'الاستثمار' workspace has its module set to 'Invstiment' and a sequence id."""
    frappe.only_for("System Manager")

    # Ensure Module Def exists
    if not frappe.db.exists("Module Def", {"module_name": "Invstiment"}):
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": "Invstiment",
            "app_name": "invstiment",
            "custom": 0,
        }).insert(ignore_if_duplicate=True)

    names = frappe.get_all("Workspace", filters={"label": "الاستثمار", "public": 1}, pluck="name")
    if not names:
        return "Workspace 'الاستثمار' not found."

    ws = frappe.get_doc("Workspace", names[0])
    changed = False
    if not ws.module:
        ws.module = "Invstiment"
        changed = True
    if not ws.sequence_id or float(ws.sequence_id) == 0.0:
        ws.sequence_id = (frappe.db.count("Workspace", {"public": 1}, cache=True) or 0) + 1
        changed = True
    if changed:
        ws.save(ignore_permissions=True)
        frappe.clear_cache()
        try:
            frappe.cache().delete_key("bootinfo")
        except Exception:
            pass
        return f"Workspace '{ws.name}' updated (module/sequence)."
    return "No changes required."


def adjust_investment_workspace_layout():
    """Ensure the workspace content contains cards pointing to link groups so the page is not empty."""
    frappe.only_for("System Manager")

    names = frappe.get_all("Workspace", filters={"label": "الاستثمار", "public": 1}, pluck="name")
    if not names:
        return "Workspace not found."
    ws = frappe.get_doc("Workspace", names[0])

    # Keep only one card group labeled 'الإدارة' and its links
    new_links = []
    found_card = False
    for l in ws.links:
        if l.type == "Card Break" and l.label == "الإدارة":
            found_card = True
            new_links.append(l)
            continue
        if found_card:
            # after the intended card, keep links until next card break
            if l.type == "Card Break":
                break
            new_links.append(l)
    if found_card and new_links:
        ws.set("links", [])
        for l in new_links:
            ws.append("links", l)

    # Build content with header + a card pointing to 'الإدارة'
    ws.content = frappe.as_json([
        {"id": "hdr1", "type": "header", "data": {"text": "<span class=\"h4\"><b>المحافظ والاستثمار</b></span>", "col": 12}},
        {"id": "sp1", "type": "spacer", "data": {"col": 12}},
        {"id": "card_admin", "type": "card", "data": {"card_name": "الإدارة", "col": 12}},
    ])

    ws.save(ignore_permissions=True)

    frappe.clear_cache()
    try:
        frappe.cache().delete_key("bootinfo")
    except Exception:
        pass
    return "Workspace layout adjusted."