import httpx
from app.config import SUPABASE_URL, SUPABASE_KEY


class UserService:

    @staticmethod
    async def user_exists(user_id: str, user_hash: str) -> tuple[bool, int, str]:
        """
            Checks if a user with the given `user_id` and `user_hash`
            exists in the `users` table.

        Returns:
            (exists, status_code, message)
        """
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{SUPABASE_URL}/rest/v1/users",
                params={
                    "and": f"(id.eq.{user_id},user_hash.eq.{user_hash})"
                },
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}"
                }
            )

            if resp.status_code != 200:
                return False, resp.status_code, resp.text

            data = resp.json()
            if not data:
                return False, 404, "User not found"

            return True, 200, "User exists"


user_service = UserService()
