import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# --- Supabase ---
# We are changing this to use the SERVICE_ROLE_KEY.
# This is the single most important security fix for your app.
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # <-- CRITICAL CHANGE

# We create one, single, secure client for the whole app
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- Google OAuth ---
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# Google API endpoints
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"


# --- Microsoft API endpoints ---
OUTLOOK_TENANT_ID = os.getenv("OUTLOOK_TENANT_ID", "common")
OUTLOOK_AUTH_URL = f"https://login.microsoftonline.com/{OUTLOOK_TENANT_ID}/oauth2/v2.0/authorize"
OUTLOOK_TOKEN_URL = f"https://login.microsoftonline.com/{OUTLOOK_TENANT_ID}/oauth2/v2.0/token"
OUTLOOK_USERINFO_URL = "https://graph.microsoft.com/v1.0/me"

OUTLOOK_CLIENT_ID = os.getenv("OUTLOOK_CLIENT_ID")
OUTLOOK_CLIENT_SECRET = os.getenv("OUTLOOK_CLIENT_SECRET")
OUTLOOK_REDIRECT_URI = os.getenv("OUTLOOK_REDIRECT_URI")


# --- XERO API ---
XERO_CLIENT_ID = os.getenv("XERO_CLIENT_ID")
XERO_CLIENT_SECRET = os.getenv("XERO_CLIENT_SECRET")
XERO_REDIRECT_URI = os.getenv("XERO_REDIRECT_URI")

XERO_AUTH_URL = "https://login.xero.com/identity/connect/authorize"
XERO_TOKEN_URL = "https://identity.xero.com/connect/token"
XERO_CONNECTIONS_URL = "https://api.xero.com/connections"


# --- QUICKBOOKS ---
QUICKBOOKS_CLIENT_ID = os.getenv("QUICKBOOKS_CLIENT_ID")
QUICKBOOKS_CLIENT_SECRET = os.getenv("QUICKBOOKS_CLIENT_SECRET")
QUICKBOOKS_REDIRECT_URI = os.getenv("QUICKBOOKS_REDIRECT_URI")

QUICKBOOKS_AUTH_URL = "https://appcenter.intuit.com/connect/oauth2"
QUICKBOOKS_TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
QUICKBOOKS_USERINFO_URL = "https://sandbox-accounts.platform.intuit.com/v1/openid_connect/userinfo"


# --- Frontend Redirects ---
FRONTEND_GOOGLE_URL = "https://invnudge.com/setup-3?service=google&status=connected"
FRONTEND_OUTLOOK_URL = "https://invnudge.com/setup-3?service=outlook&status=connected"
FRONTEND_XERO_URL = "https://invnudge.com/setup-2?service=xero&status=connected"
FRONTEND_QUICKBOOKS_URL = "https://invnudge.com/setup-2?service=quickbooks&status=connected"

# --- JWT (Not currently used by your main app, but here for completeness) ---
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"

# === END: NEW config.py CODE ===
