import jinja2
from pathlib import Path
import sys

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("GTK3 libraries not found in PATH. Ensure bin/gtk3/bin is in PATH.")
    HTML = None
    CSS = None

TEMPLATE_DIR = Path("app/templates")
STATIC_DIR = Path("app/static")

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)

def _get_template_name(style_code):
    mapping = {
        'zoho_blue': 'invoices/zoho_blue.html',
        'stripe_minimal': 'invoices/stripe_minimal.html',
        'enterprise_teal': 'invoices/enterprise_teal.html',
    }
    return mapping.get(style_code, 'invoices/zoho_blue.html')

DEFAULT_CONTEXT = {
    "company": {
        "name": "Alphabit Technologies",
        "address": "No. 12/24, 2nd Floor, Innovation Hub, Chennai, TN 600001",
        "tax_id": "33AACCA1234A1Z5"
    },
    "customer": {
        "name": "Customer Name",
        "address": "456 Customer Rd, City, Country",
        "gstin": "CUST-GSTIN"
    },
    "invoice_number": "INV-000",
    "date": "2024-02-11",
    "due_date": "2024-02-25",
    "items": [],
    "bank": {
        "bank_name": "HDFC Bank Ltd",
        "account_no": "50200012345678",
        "ifsc": "HDFC0001234",
        "account_name": "Alphabit Technologies"
    },
    "tax_rate": 18
}

def render_html(data):
    template_name = _get_template_name(data.get('template_style', 'zoho_blue'))
    template = env.get_template(template_name)

    # Merge defaults with data
    # We do a deep merge for dictionaries like 'company', 'customer', 'bank'
    # or just simple update if we assume structure matches. 
    # For simplicity, we'll just use defaults for missing top-level keys 
    # and maybe some nested ones if we want to be very safe.
    
    full_data = DEFAULT_CONTEXT.copy()
    full_data.update(data)
    
    # Ensure nested dicts are merged if partial data is provided
    for key in ['company', 'customer', 'bank']:
        if key in data and isinstance(data[key], dict):
             start_dict = DEFAULT_CONTEXT[key].copy()
             start_dict.update(data[key])
             full_data[key] = start_dict

    # --- SAFETY LOGIC: Force numbers to be floats ---
    items = full_data.get('items', [])
    safe_items = []
    subtotal = 0.0

    for item in items:
        try:
            qty = float(item.get('qty', 0))
            rate = float(item.get('rate', 0))
            item['qty'] = qty
            item['rate'] = rate
            # Ensure description exists
            if 'desc' not in item:
                 item['desc'] = item.get('description', 'Item')
            safe_items.append(item)
            subtotal += (qty * rate)
        except ValueError:
            continue

    tax_rate = float(full_data.get('tax_rate', 0))
    tax_amount = subtotal * (tax_rate / 100)
    total = subtotal + tax_amount

    context = {
        **full_data, 'items': safe_items, 'subtotal': subtotal,
        'tax_rate': tax_rate, 'tax_amount': tax_amount, 'total': total,
        'css_path': str(STATIC_DIR / 'css' / 'invoice.css')
    }
    return template.render(context)

def generate_pdf_bytes(data):
    if not HTML:
        raise ImportError("WeasyPrint GTK3 libraries not found. See README.md for installation instructions.")
    html_string = render_html(data)
    html = HTML(string=html_string, base_url=str(STATIC_DIR))
    return html.write_pdf()
