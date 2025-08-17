import base64

import httpx
from supabase import create_client
import app.config as config

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)


class OAuthService:
    async def handle_google_callback(self, code: str, user_id: str):
        """
        Handles OAuth callback for Google provider.

        Args:
            code (str): Authorization code returned by the provider.
            user_id (int): The ID of the user initiating the OAuth login.
        """
        async with httpx.AsyncClient() as client:
            token_resp = await client.post(config.GOOGLE_TOKEN_URL, data={
                "code": code,
                "client_id": config.GOOGLE_CLIENT_ID,
                "client_secret": config.GOOGLE_CLIENT_SECRET,
                "redirect_uri": config.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code"
            })
            tokens = token_resp.json()
            access_token = tokens.get("access_token")

            user_resp = await client.get(config.GOOGLE_USERINFO_URL, headers={
                "Authorization": f"Bearer {access_token}"
            })
            user_info = user_resp.json()

            supabase.table("google_users").upsert({
                "google_id": user_info["id"],
                "email": user_info["email"],
                "given_name": user_info.get("given_name"),
                "family_name": user_info.get("family_name"),
                "picture": user_info.get("picture"),
                "access_token": tokens.get("access_token"),
                "refresh_token": tokens.get("refresh_token"),
                "user_id": user_id
            }, on_conflict="user_id").execute()

    async def handle_outlook_callback(self, code: str, user_id: str):
        """
        Handles OAuth callback for Outlook provider.

        Args:
            code (str): Authorization code returned by the provider.
            user_id (int): The ID of the user initiating the OAuth login.
        """
        async with httpx.AsyncClient() as client:
            # 1. Exchange code for tokens
            token_resp = await client.post(
                config.OUTLOOK_TOKEN_URL,
                data={
                    "client_id": config.OUTLOOK_CLIENT_ID,
                    "scope": "openid profile email offline_access https://graph.microsoft.com/User.Read",
                    "code": code,
                    "redirect_uri": config.OUTLOOK_REDIRECT_URI,
                    "grant_type": "authorization_code",
                    "client_secret": config.OUTLOOK_CLIENT_SECRET
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            tokens = token_resp.json()
            access_token = tokens.get("access_token")

            # 2. Fetch user info
            user_resp = await client.get(
                config.OUTLOOK_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            user_info = user_resp.json()

        # 3. Upsert user in Supabase
        supabase.table("outlook_users").upsert({
            "outlook_id": user_info.get("id"),
            "email": user_info.get("userPrincipalName"),
            "display_name": user_info.get("displayName"),
            "given_name": user_info.get("givenName"),
            "surname": user_info.get("surname"),
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
            "user_id": user_id  # ensure we link to the correct user
        }, on_conflict="user_id").execute()

    async def handle_xero_callback(self, code: str, user_id: str):
        """
        Handles OAuth callback for Xero provider.

        Args:
            code (str): Authorization code returned by the provider.
            user_id (int): The ID of the user initiating the OAuth login.
        """
        async with httpx.AsyncClient() as client:
            basic_auth = base64.b64encode(
                f"{config.XERO_CLIENT_ID}:{config.XERO_CLIENT_SECRET}".encode()).decode()

            token_resp = await client.post(
                config.XERO_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": config.XERO_REDIRECT_URI
                },
                headers={
                    "Authorization": f"Basic {basic_auth}",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            tokens = token_resp.json()
            access_token = tokens.get("access_token")

            connections_resp = await client.get(
                config.XERO_CONNECTIONS_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            connections = connections_resp.json()

        tenant_id = connections[0].get("tenantId") if connections else None
        tenant_name = connections[0].get("tenantName") if connections else None

        supabase.table("xero_users").upsert({
            "tenant_id": tenant_id,
            "tenant_name": tenant_name,
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
            "id_token": tokens.get("id_token"),
            "user_id": user_id  # Save the user_id from state
        }, on_conflict="user_id").execute()

    async def handle_quickbooks_callback(self, code: str, realm_id: str, user_id: str):
        """
        Handles OAuth callback for QuickBooks provider.

        Args:
            code (str): Authorization code returned by QuickBooks.
            realm_id (str): The QuickBooks company (realm) ID.
            user_id (int): The ID of the user initiating the OAuth login.
        """
        async with httpx.AsyncClient() as client:
            basic_auth = base64.b64encode(
                f"{config.QUICKBOOKS_CLIENT_ID}:{config.QUICKBOOKS_CLIENT_SECRET}".encode()
            ).decode()

            token_resp = await client.post(
                config.QUICKBOOKS_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": config.QUICKBOOKS_REDIRECT_URI
                },
                headers={
                    "Authorization": f"Basic {basic_auth}",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            tokens = token_resp.json()
            access_token = tokens.get("access_token")

            user_resp = await client.get(
                config.QUICKBOOKS_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            user_info = user_resp.json()

        supabase.table("quickbooks_users").upsert({
            "realm_id": realm_id,
            "email": user_info.get("email"),
            "given_name": user_info.get("givenName"),
            "family_name": user_info.get("familyName"),
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
            "id_token": tokens.get("id_token"),
            "user_id": user_id
        }, on_conflict="user_id").execute()


oauth_service = OAuthService()
