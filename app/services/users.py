import httpx

from app.config import SUPABASE_URL, SUPABASE_KEY


class UserService:

    @staticmethod
    async def user_exists(user_id: str, user_hash: str) -> bool:
        """
            Asynchronously checks if a user with the given `user_id` and `user_hash`
            exists in the `users` table.

            Args:
                user_id (str): The UUID of the user.
                user_hash (str): The UUID-based hash associated with the user.

            Returns:
                bool: True if the user exists, otherwise False.
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
            data = resp.json()
            return bool(data)


user_service = UserService()
