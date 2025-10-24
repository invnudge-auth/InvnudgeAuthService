# === START: New file contents for app/api/status.py ===

from fastapi import APIRouter, HTTPException
from uuid import UUID

# This imports the secure supabase client from your config file
# just like your other api files (google.py, etc.) do
from app.config import supabase 

router = APIRouter()

@router.get("/auth/status")
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

# === END: New file contents ===
