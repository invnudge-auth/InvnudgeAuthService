from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import google, outlook, xero, quickbooks

app = FastAPI(
    title="Invnudge OAuth API",
    version="1.0.0",
    description="API for handling OAuth2 authentication with Supabase integration."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(google.router)
app.include_router(outlook.router)
app.include_router(xero.router)
app.include_router(quickbooks.router)
