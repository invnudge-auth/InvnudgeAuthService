from fastapi import APIRouter, Query, Depends
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
import urllib.parse
from supabase import create_client
import app.config as config
from app.api.dependencies import get_user_service
from app.services.OAuthService import oauth_service
from app.services.users import UserService

router = APIRouter(tags=["Google OAuth"])

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)


@router.get("/auth/google")
async def google_login(
        user_id: str = Query(...),
        user_service: UserService = Depends(get_user_service)
):
    """
    Initiates the Google OAuth2 login process.

    This endpoint redirects the user to the Google OAuth2 consent screen,
    requesting access to their email, profile, and basic account information.

    Args:
        user_id (str): The ID of the user initiating the OAuth login.
                       Passed via the 'state' parameter to track the user.
        user_service: service for checking existing user
    Returns:
        RedirectResponse: Redirects to Google's OAuth2 login page.
    """
    if not await user_service.user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return RedirectResponse(
        f"{config.GOOGLE_AUTH_URL}?client_id={config.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={urllib.parse.quote(config.GOOGLE_REDIRECT_URI)}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
        f"&prompt=consent"
        f"&state={user_id}"
    )


@router.get("/auth/google/callback")
async def google_callback(code: str, state: str):
    """
    Handles Google OAuth2 callback after user authentication.

    Steps:
        1. Exchanges the authorization code for access and refresh tokens.
        2. Fetches the user's profile information from Google.
        3. Stores or updates the user in the Supabase `google_users` table.
        4. (Optional) Creates a JWT token for the user.
        5. Redirects the user back to the frontend application.

    Args:
        code (str): Authorization code returned by Google.
        state (str): User ID passed through the 'state' parameter.

    Returns:
        RedirectResponse: Redirects to the frontend with authentication status.
    """
    await oauth_service.handle_google_callback(code, state)
    return RedirectResponse(url=config.FRONTEND_GOOGLE_URL)
