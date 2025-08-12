import json
import os
import frappe


def ensure_module_def(module_name: str = "Invstiment"):
    """Ensure Module Def exists for this app/module."""
    if not frappe.db.exists("Module Def", {"module_name": module_name}):
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": module_name,
            "app_name": "invstiment",
            "custom": 0,
        }).insert(ignore_if_duplicate=True)


def sync_investment_workspace():
    """Create or update the 'investment' Workspace from JSON file."""
    frappe.only_for(("System Manager",))

    ensure_module_def("Invstiment")

    # Prefer nested workspace path (app/module/workspace/<name>/<name>.json)
    nested = frappe.get_app_path(
        "invstiment", "invstiment", "invstiment", "workspace", "investment", "investment.json"
    )
    flat = frappe.get_app_path(
        "invstiment", "invstiment", "invstiment", "workspace", "investment.json"
    )

    json_path = nested if os.path.exists(nested) else flat
    if not os.path.exists(json_path):
        return f"Workspace JSON not found at: {nested} or {flat}"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Normalize mandatory fields
    data.setdefault("doctype", "Workspace")
    data.setdefault("name", "investment")
    data.setdefault("module", "Invstiment")
    data.setdefault("public", 1)
    data.setdefault("is_hidden", 0)

    # Upsert Workspace
    existing = frappe.db.exists("Workspace", data.get("name"))
    doc = frappe.get_doc(data)
    if existing:
        # Keep same name, update fields
        doc.flags.ignore_mandatory = True
        doc.flags.ignore_permissions = True
        # Load existing and update values
        existing_doc = frappe.get_doc("Workspace", data.get("name"))
        for field, value in data.items():
            if field in ("doctype", "name"):  # doctype/name immutable
                continue
            setattr(existing_doc, field, value)
        existing_doc.save()
        msg = "updated"
    else:
        doc.flags.ignore_permissions = True
        doc.insert()
        msg = "created"

    # Clear caches so it shows up immediately
    frappe.clear_cache(user=frappe.session.user)
    frappe.cache().delete_keys_with_pattern("desk_sidebar_items*")

    return f"Workspace '{data.get('name')}' {msg} from {os.path.relpath(json_path)}"
