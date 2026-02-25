from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from manager.service_manager import ServiceManager
from manager.db import DatabaseManager
import os

app = FastAPI()

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
