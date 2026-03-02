import requests
import os

# Java team API endpoints — override via environment variables if needed
INVOICE_API_URL = os.getenv(
    "INVOICE_API_URL",
    "https://api-bi-buysell-service-ind.u-clo.com/owner-0.0.1/api/Reports/invoice"
)
SALES_API_URL = os.getenv(
    "SALES_API_URL",
    "https://api-bi-buysell-service-ind.u-clo.com/owner-0.0.1/api/Reports/sales"
)


def fetch_invoice_data(invoice_no, plant="test"):
    """
    Fetches invoice data from the Java API.
    Use invoice_no = "MOCK-001" to get mock data without hitting the API.
    Java API: GET /api/Reports/invoice?invoiceNo=IN05250000011&plant=test
    """
    # --- MOCK MODE (used for testing/demo) ---
    if invoice_no == "MOCK-001":
        return {
            "invoice_number": "MOCK-001",
            "date": "2024-02-12",
            "due_date": "2024-02-28",
            "customer": {
                "name": "Demo Customer Pvt Ltd",
                "address": "123 Mock Street, Innovation Park, Tech City",
                "gstin": "29ABCDE1234F1Z5",
                "email": "contact@democustomer.com",
                "phone": "+91 98765 43210"
            },
            "items": [
                {"desc": "Mock Service Item A", "notes": "Test service description", "hsn": "998311", "qty": 1, "rate": 5000.00, "tax_type": "IGST"},
                {"desc": "Mock Hardware Item B", "notes": "Test hardware description", "hsn": "851762", "qty": 10, "rate": 150.00, "tax_type": "IGST"}
            ],
            "tax_rate": 18
        }
    # -----------------------------------------

    params = {"invoiceNo": invoice_no, "plant": plant}
    response = requests.get(INVOICE_API_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    if data is None:
        raise ValueError(f"API returned no data for invoice {invoice_no}")
    if data.get("statusCode") != 200 or "results" not in data:
        raise ValueError(f"Failed to fetch invoice: {data.get('message', 'Unknown error')}")

    results = data.get("results")
    if results is None:
        raise ValueError(f"No data found for invoice {invoice_no}")

    hdr     = results.get("invoiceHdr", {})
    cust    = results.get("customer", {})
    details = results.get("invoiceDetList", [])

    return {
        "invoice_number": hdr.get("invoiceNo"),
        "date":           hdr.get("invoiceDate"),
        "due_date":       hdr.get("dueDate", hdr.get("invoiceDate")),
        "customer": {
            "name":    cust.get("customerName"),
            "address": f"{cust.get('addressROne','')} {cust.get('addressRTwo','')} {cust.get('addressRThree','')} {cust.get('addressRFour','')}".strip(),
            "gstin":   cust.get("rcbNo", "N/A"),
            "email":   cust.get("email"),
            "phone":   cust.get("telephoneNo")
        },
        "items": [
            {
                "desc":     item.get("item"),
                "notes":    item.get("note"),
                "hsn":      "N/A",
                "qty":      item.get("qty", 0),
                "rate":     item.get("unitPrice", 0),
                "tax_type": item.get("taxType")
            } for item in details
        ],
        "tax_rate": hdr.get("outboundGst", 0)
    }


def fetch_sales_data(do_no, plant="test"):
    """
    Fetches sales order data from the Java API.
    Use do_no = "MOCK-001" to get mock data without hitting the API.
    Java API: GET /api/Reports/sales?doNO=S01250000108&plant=test
    """
    # --- MOCK MODE ---
    if do_no == "MOCK-001":
        return {
            "invoice_number": "MOCK-SO-001",
            "date": "2024-02-12",
            "due_date": "2024-02-15",
            "customer": {
                "name": "Demo Sales Client",
                "address": "456 Sales Road, Market Town",
                "gstin": "33XYZAB9876L1Z2"
            },
            "items": [
                {"desc": "Mock Sales Item 1", "notes": "Urgent delivery", "qty": 50, "rate": 200.00},
                {"desc": "Mock Sales Item 2", "notes": "Standard packaging", "qty": 20, "rate": 550.00}
            ]
        }
    # ------------------

    params = {"doNO": do_no, "plant": plant}
    response = requests.get(SALES_API_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    if data is None:
        raise ValueError(f"API returned no data for sales order {do_no}")
    if data.get("statusCode") != 200 or "results" not in data:
        raise ValueError(f"Failed to fetch sales order: {data.get('message', 'Unknown error')}")

    results = data.get("results")
    if results is None:
        raise ValueError(f"No data found for sales order {do_no}")

    hdr     = results.get("doHdr", {})
    cust    = results.get("customer", {})
    details = results.get("dodetList", [])

    return {
        "invoice_number": hdr.get("doNo"),
        "date":           hdr.get("delDate"),
        "due_date":       hdr.get("collectionDate"),
        "customer": {
            "name":    cust.get("customerName"),
            "address": f"{cust.get('addressROne','')} {cust.get('addressRTwo','')} {cust.get('addressRThree','')} {cust.get('addressRFour','')}".strip(),
            "gstin":   cust.get("rcbNo", "N/A")
        },
        "items": [
            {
                "desc":  item.get("itemDescription", item.get("item")),
                "notes": item.get("userFieldOne"),
                "qty":   item.get("quantityIs", 0),
                "rate":  item.get("unitPrice", 0)
            } for item in details
        ]
    }
