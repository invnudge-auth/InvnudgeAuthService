from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.config import supabase

router = APIRouter()

@router.get("/auth/status")
async def get_user_status(user_id: UUID):
    """
    Securely fetches a user's onboarding status for Framer.
    Uses service_role key to bypass RLS.
    """
    try:
        response = supabase.table('users') \
                           .select('name, email, status, email_provider, invoice_provider') \
                           .eq('id', str(user_id)) \
                           .single() \
                           .execute()

        if response.data:
            return response.data
        else:
            raise HTTPException(status_code=404, detail="User not found")
            
    except Exception as e:
        print(f"Error fetching user status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
