import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Test Raw Invoice JSON
invoice_raw = {
    "results": {
        "invoiceHdr": {
            "plant": "TEST",
            "invoice": "IN05250000011",
            "invoiceDate": "26/05/2025",
            "currencyId": "INR",
            "jobNum": "dfgdffdgdf"
        },
        "invoiceDetList": [
            {
                "item": "GM_2F_056",
                "qty": 1.0,
                "unitPrice": 799.0,
                "taxType": "TCS [0.0%]"
            }
        ],
        "customer": {
            "customerName": "CASH",
            "addressROne": "Chennai Office",
            "state": "Tamil Nadu",
            "country": "India"
        }
    }
}

print("Testing Raw Invoice JSON POST...")
resp = requests.post(f"{BASE_URL}/api/v1/process/invoice-json", json=invoice_raw)
if resp.status_code == 200:
    print("[OK] Raw Invoice JSON processed successfully!")
    with open("test_raw_invoice.pdf", "wb") as f:
        f.write(resp.content)
    print("   Saved to test_raw_invoice.pdf")
else:
    print(f"[ERROR] Failed: {resp.status_code}")
    print(resp.text)

# 2. Test Raw Sales JSON
sales_raw = {
    "results": {
        "doHdr": {
            "doNo": "S01250000108",
            "delDate": "11/01/2025",
            "currencyId": "INR"
        },
        "dodetList": [
            {
                "itemDescription": "P0001 DESC",
                "quantityIs": 1.0,
                "unitPrice": 50.0,
                "userFieldOne": "P0001 DESC"
            }
        ],
        "customer": {
            "customerName": "ALIALHASHEMI TRADING COMPANY LLC",
            "addressROne": "Sheikh Zayed Road,"
        }
    }
}

print("\nTesting Raw Sales JSON POST...")
resp = requests.post(f"{BASE_URL}/api/v1/process/sales-json", json=sales_raw)
if resp.status_code == 200:
    print("[OK] Raw Sales JSON processed successfully!")
    with open("test_raw_sales.pdf", "wb") as f:
        f.write(resp.content)
    print("   Saved to test_raw_sales.pdf")
else:
    print(f"[ERROR] Failed: {resp.status_code}")
    print(resp.text)
