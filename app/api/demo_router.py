from fastapi import APIRouter, Response
from app.services.pdf_service import generate_pdf_bytes

router = APIRouter(prefix="/api/v1/demo")

DEMO_SCENARIOS = {
    "short": {
        "invoice_number": "DEMO-SHORT-001",
        "date": "2024-02-11",
        "due_date": "2024-02-25",
        "customer": {
            "name": "Quick Mart Solutions",
            "address": "45 Retail Ave, Chennai",
            "gstin": "33ABCDE1234F1Z5"
        },
        "items": [
            {"desc": "Software License", "qty": 1, "rate": 5000.00, "hsn": "997331"}
        ]
    },
    "long_desc": {
        "invoice_number": "DEMO-DESC-002",
        "date": "2024-02-11",
        "due_date": "2024-02-25",
        "customer": {
            "name": "Global Tech Industries",
            "address": "Tower C, SEZ Zone, Bangalore, KA 560100",
            "gstin": "29AABCG1234H1Z1"
        },
        "items": [
            {
                "desc": "Annual Managed Security Services & Vulnerability Assessment",
                "notes": "Includes 24/7 monitoring, monthly penetration testing, incident response drills, and priority support for all regional offices. Service period: April 2024 - March 2025. This contract includes quarterly review meetings and on-site emergency support if required for critical infrastructure failures.",
                "qty": 1, "rate": 150000.00, "hsn": "998313"
            },
            {
                "desc": "Cloud Migration Fee",
                "notes": "Migration of legacy databases to AWS Aurora. Includes data cleanup and validation.",
                "qty": 40, "rate": 1200.00, "hsn": "998322"
            }
        ]
    },
    "many_items": {
        "invoice_number": "DEMO-MANY-003",
        "date": "2024-02-11",
        "due_date": "2024-02-25",
        "customer": {
            "name": "Mega Wholesale Hub",
            "address": "Plot #10, Industrial Estate, Salem, TN",
            "gstin": "33AAACH9988G1Z0"
        },
        "items": [
            {"desc": f"Inventory SKU-A{i:03d}", "notes": "Bulk packing", "qty": 10, "rate": 45.00, "hsn": "8471"}
            for i in range(1, 26) # 25 items to force multiple pages
        ]
    }
}

@router.get("/{scenario}")
async def get_demo(scenario: str, template: str = "zoho_blue"):
    data = DEMO_SCENARIOS.get(scenario)
    if not data:
        return Response(content="Scenario not found. Use 'short', 'long_desc', or 'many_items'", status_code=404)
    
    data['template_style'] = template
    pdf_bytes = generate_pdf_bytes(data)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=demo_{scenario}.pdf"}
    )
