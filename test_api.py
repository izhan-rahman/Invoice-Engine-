import urllib.request
import urllib.error
import json

BASE_URL = "https://alpha-invoice-engine.onrender.com"

def test_endpoint(method, path, data=None):
    url = BASE_URL + path
    headers = {}
    if data:
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            content_type = response.headers.get('Content-Type', '')
            print(f"[{method}] {path} -> Status: {status} OK (Content-Type: {content_type})")
            
            # Print a snippet of the response for JSON or text
            if 'json' in content_type or 'text' in content_type:
                body = response.read(200).decode('utf-8', errors='ignore')
                print(f"  body snippet: {body!r}")
            elif 'pdf' in content_type:
                print(f"  body: [PDF File Content]")
                
    except urllib.error.HTTPError as e:
        print(f"[{method}] {path} -> Status: {e.code} {e.reason}")
        try:
            body = e.read(200).decode('utf-8', errors='ignore')
            print(f"  error body snippet: {body!r}")
        except:
            pass
    except Exception as e:
        print(f"[{method}] {path} -> Error: {e}")

print("--- Testing API Endpoints ---")
test_endpoint("GET", "/")
test_endpoint("GET", "/docs")
test_endpoint("GET", "/api/v1/demo/1")  # Testing with scenario '1'
test_endpoint("GET", "/api/v1/generate/invoice/INV-001") # Dummy invoice
test_endpoint("POST", "/preview", data={"template_id": "test", "data": {}}) # Dummy payload
test_endpoint("POST", "/download", data={"template_id": "test", "data": {}}) # Dummy payload
