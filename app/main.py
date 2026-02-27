from fastapi import FastAPI, Request, BackgroundTasks, Query
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.services.pdf_service import generate_pdf_bytes
from app.services.data_service import fetch_invoice_data, fetch_sales_data
from app.api.demo_router import router as demo_router
import requests

app = FastAPI(title="Invoice Engine Pro")
app.include_router(demo_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("ui/index.html", {"request": request})

# --- EXTERNAL INTEGRATION ENDPOINTS ---

@app.get("/api/v1/generate/invoice/{invoice_no}")
async def generate_from_external_invoice(
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
async def generate_from_external_sales(
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
async def preview_invoice(request: Request):
    data = await request.json()
    pdf_bytes = generate_pdf_bytes(data)
    return Response(content=pdf_bytes, media_type="application/pdf")

@app.post("/download")
async def download_invoice(request: Request):
    data = await request.json()
    pdf_bytes = generate_pdf_bytes(data)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=invoice.pdf"})
