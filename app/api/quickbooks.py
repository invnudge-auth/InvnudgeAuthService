from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

from app.api.dependencies import get_user_service
from app.config import (
    QUICKBOOKS_AUTH_URL,
    QUICKBOOKS_CLIENT_ID,
    QUICKBOOKS_REDIRECT_URI,
    FRONTEND_QUICKBOOKS_URL
)
from app.services.users import UserService
from app.services.OAuthService import oauth_service

load_dotenv()

router = APIRouter(tags=["QuickBooks OAuth"])


@router.get("/auth/quickbooks")
async def quickbooks_auth(
        user_id: str = Query(...),
        user_hash: str = Query(...),
        user_service: UserService = Depends(get_user_service)):
    """
    Initiates the QuickBooks OAuth2 login process.

    This endpoint redirects the user to the QuickBooks consent screen,
    requesting access to accounting, profile, email, phone and address info.

    Args:
        user_id (int): The ID of the user initiating the OAuth login.
                       Passed via 'state' parameter to link QuickBooks account
                       to the correct application user.
        user_hash (str): A UUID-based hash associated with the user, used for
            additional verification and passed via the 'state' parameter.
        user_service (UserService): Service for checking existing user.

    Returns:
        RedirectResponse: Redirects to QuickBooks OAuth2 login/consent page.
    """
    exists, status, message = await user_service.user_exists(user_id, user_hash)

    if not exists:
        raise HTTPException(status_code=status, detail=message)

    scope = "com.intuit.quickbooks.accounting openid profile email phone address"

    return RedirectResponse(
        f"{QUICKBOOKS_AUTH_URL}?response_type=code"
        f"&client_id={QUICKBOOKS_CLIENT_ID}"
        f"&redirect_uri={QUICKBOOKS_REDIRECT_URI}"
        f"&scope={scope}"
        f"&state={user_id}"
    )


@router.get("/auth/quickbooks/callback")
async def quickbooks_callback(
        code: str,
        realmId: str,
        state: int = Query(...)):
    """
    Handles QuickBooks OAuth2 callback after user authentication.

    Steps:
        1. Exchanges the authorization code for access and refresh tokens.
        2. Fetches the user's profile information from QuickBooks.
        3. Stores or updates the user in the Supabase `quickbooks_users` table.
           Uses the `user_id` passed via the 'state' parameter to upsert.
        4. Redirects the user back to the frontend application.

    Args:
        code (str): Authorization code returned by QuickBooks.
        realmId (str): QuickBooks company (realm) ID.
        state (int): User ID passed through the 'state' parameter.

    Returns:
        RedirectResponse: Redirects to frontend with authentication status.
    """
    await oauth_service.handle_quickbooks_callback(code, realmId, state)
    return RedirectResponse(url=FRONTEND_QUICKBOOKS_URL)
