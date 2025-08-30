from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

from app.api.dependencies import get_user_service
from app.config import (
    OUTLOOK_AUTH_URL,
    OUTLOOK_CLIENT_ID,
    OUTLOOK_REDIRECT_URI,
    FRONTEND_OUTLOOK_URL
)
from app.services.OAuthService import oauth_service
from app.services.users import UserService

load_dotenv()

router = APIRouter(tags=["Outlook OAuth"])


@router.get("/auth/outlook")
async def outlook_auth(
        state: str = Query(...),
        user_service: UserService = Depends(get_user_service)):
    """
    Initiates the Outlook OAuth2 login process.

    This endpoint redirects the user to the Outlook consent screen,
    requesting access to profile, email, and basic account information.

    Args:
        state (str): Current user state.
        user_service (UserService): Service for checking existing user.

    Returns:
        RedirectResponse: Redirects to Microsoft's OAuth2 login page.
    """
    user = state.split('/')
    # first part is user_id, second one is user_hash
    exists, status, message = await user_service.user_exists(user[0], user[-1])

    if not exists:
        raise HTTPException(status_code=status, detail=message)
    return RedirectResponse(
        f"{OUTLOOK_AUTH_URL}?client_id={OUTLOOK_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={OUTLOOK_REDIRECT_URI}"
        f"&response_mode=query"
        f"&scope=openid profile email offline_access Mail.Read Mail.ReadWrite Mail.Send"
        f"&state={state}"
    )


@router.get("/auth/outlook/callback")
async def outlook_callback(code: str, state: str = Query(...)):
    """
    Handles Outlook OAuth2 callback after user authentication.

    Steps:
        1. Exchanges the authorization code for access and refresh tokens.
        2. Fetches the user's profile information from Microsoft Graph.
        3. Stores or updates the user in the Supabase `outlook_users` table.
           Uses the `user_id` passed via the 'state' parameter to upsert.
        4. Redirects the user back to the frontend application (currently localhost).

    Args:
        code (str): Authorization code returned by Outlook.
        state (int): User ID and hash passed through the 'state' parameter.

    Returns:
        RedirectResponse: Redirects to frontend with authentication status.
    """
    await oauth_service.handle_outlook_callback(code, state)
    return RedirectResponse(url=FRONTEND_OUTLOOK_URL+f'&state={state}')
