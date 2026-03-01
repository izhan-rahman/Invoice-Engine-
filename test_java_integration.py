import urllib.request
import urllib.error
import json
import os

BASE_URL = "https://alpha-invoice-engine.onrender.com"

def save_pdf_from_endpoint(endpoint_path, filename):
    url = BASE_URL + endpoint_path
    req = urllib.request.Request(url, method="GET")
    
    print(f"Fetching from: {url}")
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            content_type = response.headers.get('Content-Type', '')
            
            if 'pdf' in content_type:
                with open(filename, 'wb') as f:
                    f.write(response.read())
                print(f"  -> Success! Saved PDF to: {os.path.abspath(filename)}")
            else:
                print(f"  -> Error: Expected a PDF, but got {content_type}")
                body = response.read(200).decode('utf-8', errors='ignore')
                print(f"  -> Body snippet: {body!r}")
                
    except urllib.error.HTTPError as e:
        print(f"  -> Failed with Status {e.code}: {e.reason}")
        try:
            body = e.read(200).decode('utf-8', errors='ignore')
            print(f"  -> Error snippet: {body!r}")
        except:
            pass
    except Exception as e:
        print(f"  -> Request failed: {e}")

print("--- Testing Integration with Java API ---")

# 1. Test Sales Order endpoint with Java Team's data
print("\n[Test 1] Generating Sales Order PDF (DO: S01250000108, Plant: test)")
save_pdf_from_endpoint("/api/v1/generate/sales/S01250000108?plant=test", "SalesOrder_S01250000108_Test.pdf")

# 2. Test Invoice endpoint with Java Team's data
print("\n[Test 2] Generating Invoice PDF (Invoice: IN05250000011, Plant: test)")
save_pdf_from_endpoint("/api/v1/generate/invoice/IN05250000011?plant=test", "Invoice_IN05250000011_Test.pdf")

print("\n--- Testing Complete ---")
