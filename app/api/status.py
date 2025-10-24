# File: app/api/status.py

from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import Optional
from app.config import supabase

router = APIRouter()

@router.get("/auth/status")
async def get_user_status(
    user_id: Optional[UUID] = Query(None),
    session_id: Optional[str] = Query(None)
):
    """
    Securely fetches a user's data for Framer.
    Accepts either user_id OR session_id.
    Uses service_role key to bypass RLS.
    """
    if not user_id and not session_id:
        raise HTTPException(status_code=400, detail="Either user_id or session_id is required")
    
    try:
        query = supabase.table('users').select('id, user_hash, name, email, status, email_provider, invoice_provider')
        
        if user_id:
            query = query.eq('id', str(user_id))
        else:
            query = query.eq('session_id', session_id)
        
        response = query.single().execute()

        if response.data:
            return response.data
        else:
            raise HTTPException(status_code=404, detail="User not found")
            
    except Exception as e:
        print(f"Error fetching user status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
