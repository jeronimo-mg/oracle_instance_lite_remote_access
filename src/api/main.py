from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import shutil

# Add the 'src' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from manager.service_manager import ServiceManager
from manager.db import DatabaseManager

app = FastAPI()

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard/dist")
NOVNC_DIR = "/usr/share/novnc"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Enable CORS for the React dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
db_path = os.environ.get("DB_PATH", "litemode.db")
db = DatabaseManager(db_path)
db.init_db()

service_names = ['weston.service', 'novnc.service', 'tailscaled.service']
manager = ServiceManager(services=service_names)

@app.get("/services")
async def get_services():
    return manager.get_all_statuses()

@app.post("/services/{name}/restart")
async def restart_service(name: str):
    if name not in service_names:
        raise HTTPException(status_code=404, detail="Service not found")
    
    success = manager.restart_service(name)
    if success:
        db.add_log(name, "Service restarted via Dashboard")
        return {"status": "success"}
    else:
        raise HTTPException(status_code=500, detail="Failed to restart service")

@app.get("/logs")
async def get_logs(limit: int = 50):
    return db.get_logs(limit=limit)

# --- File Transfer Endpoints ---

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    db.add_log("system", f"File uploaded: {file.filename}")
    return {"filename": file.filename, "status": "success"}

@app.get("/files")
async def list_files():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=filename)

# --- Static Content ---

# Root redirect to dashboard
@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard/index.html")

# Serve noVNC at /desktop
if os.path.exists(NOVNC_DIR):
    app.mount("/desktop", StaticFiles(directory=NOVNC_DIR, html=True), name="desktop")

# Serve Dashboard at /dashboard
if os.path.exists(DASHBOARD_DIR):
    app.mount("/dashboard", StaticFiles(directory=DASHBOARD_DIR, html=True), name="dashboard")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
