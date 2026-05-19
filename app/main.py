from fastapi import FastAPI, Request, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.services.pdf_service import generate_pdf_bytes
from app.services.data_service import (
    fetch_invoice_data, 
    fetch_sales_data,
    process_raw_invoice_json,
    process_raw_sales_json
)
from app.api.demo_router import router as demo_router
import os
import sys
from pathlib import Path

# --- DYNAMIC PATH RESOLUTION ---
BASE_PATH = Path(getattr(sys, '_MEIPASS', os.getcwd()))

import requests

app = FastAPI(title="Invoice Engine Pro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(demo_router)

app.mount("/static", StaticFiles(directory=str(BASE_PATH / "app" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_PATH / "app" / "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("ui/index.html", {"request": request})

# --- EXTERNAL INTEGRATION ENDPOINTS ---

@app.get("/api/v1/generate/invoice/{invoice_no}")
def generate_from_external_invoice(
    invoice_no: str, 
    template: str = "zoho_blue",
    plant: str = "test"
):
    """Fetches data from Java API and returns a professional PDF"""
    try:
        # 1. Fetch
        data = fetch_invoice_data(invoice_no, plant)
        data['template_style'] = template
        
        # 2. Generate
        pdf_bytes = generate_pdf_bytes(data)
        
        # 3. Return as stream
        filename = f"Invoice_{invoice_no}.pdf"
        return Response(
            content=pdf_bytes, 
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={filename}"
            }
        )
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.get("/api/v1/generate/sales/{do_no}")
def generate_from_external_sales(
    do_no: str, 
    template: str = "zoho_blue",
    plant: str = "test"
):
    """Fetches sales order data from Java API and returns a professional PDF"""
    try:
        data = fetch_sales_data(do_no, plant)
        data['template_style'] = template
        pdf_bytes = generate_pdf_bytes(data)
        
        filename = f"SalesOrder_{do_no}.pdf"
        return Response(
            content=pdf_bytes, 
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename={filename}"}
        )
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.get("/api/v1/debug/invoice/{invoice_no}")
async def debug_external_invoice(invoice_no: str, plant: str = "test"):
    """Fetches raw data from API to inspect mapping"""
    try:
        data = fetch_invoice_data(invoice_no, plant)
        return data
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.get("/api/v1/debug/sales/{do_no}")
async def debug_external_sales(do_no: str, plant: str = "test"):
    """Fetches raw sales data from API to inspect mapping"""
    try:
        data = fetch_sales_data(do_no, plant)
        return data
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# --- TRADITIONAL ENDPOINTS ---



@app.post("/preview")
def preview_invoice(data: dict):
    pdf_bytes = generate_pdf_bytes(data)
    return Response(content=pdf_bytes, media_type="application/pdf")



@app.post("/download")
def download_invoice(data: dict):
    pdf_bytes = generate_pdf_bytes(data)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=invoice.pdf"})

# --- RAW JSON INPUT ENDPOINTS ---

@app.post("/api/v1/process/invoice-json")
async def process_invoice_json(data: dict):
    """Processes raw Invoice JSON and returns a PDF"""
    try:
        mapped_data = process_raw_invoice_json(data)
        # Add a default template if not provided
        if 'template_style' not in mapped_data:
            mapped_data['template_style'] = 'zoho_blue'
            
        pdf_bytes = generate_pdf_bytes(mapped_data)
        return Response(
            content=pdf_bytes, 
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=invoice.pdf"}
        )
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.post("/api/v1/process/sales-json")
async def process_sales_json(data: dict):
    """Processes raw Sales Order JSON and returns a PDF"""
    try:
        mapped_data = process_raw_sales_json(data)
        if 'template_style' not in mapped_data:
            mapped_data['template_style'] = 'zoho_blue'
            
        pdf_bytes = generate_pdf_bytes(mapped_data)
        return Response(
            content=pdf_bytes, 
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=sales_order.pdf"}
        )
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    # Use frozen=True for pyinstaller compatibility or simply run
    uvicorn.run(app, host="0.0.0.0", port=8000)
