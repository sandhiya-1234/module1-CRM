# app/main.py
from fastapi import FastAPI
from app.api.leads import router as leads_router

app = FastAPI(title="Pod B - CRM API")
app.include_router(leads_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
