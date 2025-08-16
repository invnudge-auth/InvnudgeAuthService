import httpx

from app.config import SUPABASE_URL, SUPABASE_KEY


class UserService:

    @staticmethod
    async def user_exists(user_id: str) -> bool:
        """
        Asynchronously checks if a user with the given `user_id` exists in the `users` table.
        Returns True if the user exists, otherwise False.
        """
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{SUPABASE_URL}/rest/v1/users",
                params={"id": f"eq.{user_id}"},
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}"
                }
            )
            data = resp.json()
            return bool(data)


user_service = UserService()
