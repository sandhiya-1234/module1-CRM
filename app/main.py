# app/main.py
from sys import audit
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.api.leads import router as leads_router
from app.api import invoices
from app.api import audit, security
from app.api import inventory
from app.api.api_v1 import messaging as messaging_router



app = FastAPI(title="Pod B - CRM API")

app.include_router(leads_router)
app.include_router(invoices.router)
app.include_router(audit.router)
#app.include_router(finance.router)
app.include_router(security.router)   
app.include_router(inventory.router)
app.include_router(messaging_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
