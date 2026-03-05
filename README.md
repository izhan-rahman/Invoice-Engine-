# Alphabit AI PDF Generation Engine

A FastAPI microservice that fetches invoice/sales data from the Java backend API and returns professional PDF documents.

Built with: **FastAPI + Jinja2 + WeasyPrint**

---

## 🚀 Deploy on Linux (E2E Cloud)

### 1. Prerequisites (run once)
```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin curl
sudo systemctl start docker && sudo systemctl enable docker
```

### 2. Clone & Deploy
```bash
git clone <your-repo-url>
cd Alphabit_AI_PDF_Generation-Engine-main

chmod +x deploy.sh
bash deploy.sh
```

The app will be live at: `http://YOUR_SERVER_IP:8000`

---

## 📡 API Endpoints

### Generate Invoice PDF
```
GET /api/v1/generate/invoice/{invoice_no}?template=zoho_blue&plant=test
```
**Example:**
```
GET http://YOUR_SERVER_IP:8000/api/v1/generate/invoice/IN05250000011?plant=test
```

### Generate Sales Order PDF
```
GET /api/v1/generate/sales/{do_no}?template=zoho_blue&plant=test
```
**Example:**
```
GET http://YOUR_SERVER_IP:8000/api/v1/generate/sales/S01250000108?plant=test
```

### Test with Mock Data (no Java API needed)
```
GET /api/v1/generate/invoice/MOCK-001
GET /api/v1/generate/sales/MOCK-001
```

### Demo PDFs
```
GET /api/v1/demo/short
GET /api/v1/demo/long_desc
GET /api/v1/demo/many_items
```

### Debug (see raw data, no PDF)
```
GET /api/v1/debug/invoice/{invoice_no}
GET /api/v1/debug/sales/{do_no}
```

### Template Options
| Value | Style |
|-------|-------|
| `zoho_blue` | Professional blue (default) |
| `stripe_minimal` | Clean minimal |
| `enterprise_teal` | Enterprise teal |

---

## 🔧 Useful Commands

```bash
# View logs
docker compose logs -f invoice-engine

# Restart
docker compose restart invoice-engine

# Stop
docker compose down

# Rebuild after code changes
docker compose up --build -d
```

---

## 🔗 Java API Sources

| Type | URL |
|------|-----|
| Invoice | `` |
| Sales | `` |
