from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from supabase import create_client
from dotenv import load_dotenv
import base64

from app.config import (
    SUPABASE_URL,
    SUPABASE_KEY,
    XERO_AUTH_URL,
    XERO_TOKEN_URL,
    XERO_CONNECTIONS_URL,
    XERO_CLIENT_ID,
    XERO_CLIENT_SECRET,
    XERO_REDIRECT_URI, FRONTEND_XERO_URL
)
from app.services.OAuthService import oauth_service
from app.services.users import user_service

load_dotenv()
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter(tags=["Xero OAuth"])


@router.get("/auth/xero")
async def xero_auth(user_id: str):
    """
    Initiates the Xero OAuth2 login process.

    Args:
        user_id (str): The ID of the user initiating the OAuth login.
                       Passed via the 'state' parameter to track the user.

    Returns:
        RedirectResponse: Redirects the user to Xero's OAuth2 authorization page.
    """
    if not await user_service.user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return RedirectResponse(
        f"{XERO_AUTH_URL}?response_type=code"
        f"&client_id={XERO_CLIENT_ID}"
        f"&redirect_uri={XERO_REDIRECT_URI}"
        f"&scope=openid profile email offline_access accounting.transactions accounting.contacts"
        f"&state={user_id}"  # Track the user
    )


@router.get("/auth/xero/callback")
async def xero_callback(code: str, state: str):
    """
    Handles the Xero OAuth2 callback after user authentication.

    Steps:
        1. Exchanges the authorization code for access and refresh tokens.
        2. Retrieves the list of connected organizations (tenants).
        3. Stores or updates the user in the Supabase `xero_users` table.
        4. Redirects the user back to the frontend application.

    Args:
        code (str): Authorization code returned by Xero.
        state (str): User ID passed through the 'state' parameter for tracking.

    Returns:
        RedirectResponse: Redirects to the frontend with authentication status.
    """
    await oauth_service.handle_xero_callback(code, state)
    return RedirectResponse(url=FRONTEND_XERO_URL)
