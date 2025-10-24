# === START: NEW main.py CODE ===

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api import google, outlook, xero, quickbooks
from uuid import UUID

# --- NEW: Import the secure Supabase client from config.py ---
from config import supabase 

app = FastAPI(
    title="Invnudge OAuth API",
    version="1.0.0",
    description="API for handling OAuth2 authentication with Supabase integration."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # You can make this stricter later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NEW: Framer Status Endpoint ---
@app.get("/auth/status")
async def get_user_status(user_id: UUID):
    """
    Securely fetches a user's onboarding status for Framer.
    """
    try:
        response = supabase.table('users') \
                           .select('name', 'email', 'status', 'email_provider', 'invoice_provider') \
                           .eq('id', user_id) \
                           .single() \
                           .execute()

        if response.data:
            return response.data
        else:
            raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        print(f"Error fetching user status: {e}") # For logging
        raise HTTPException(status_code=500, detail="Internal server error")
# --- END NEW ---


# --- Your existing routers ---
app.include_router(google.router)
app.include_router(outlook.router)
app.include_router(xero.router)
app.include_router(quickbooks.router)

# === END: NEW main.py CODE ===
