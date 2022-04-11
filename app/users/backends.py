from starlette.authentication import (
    AuthenticationBackend,
    SimpleUser,
    UnauthenticatedUser,
    AuthCredentials
)

from . import auth


class JWTCookieBackend(AuthenticationBackend):
    async def authenticate(self, request):
        session_id = request.cookies.get("session_id")
        user_data = auth.verify_user(session_id)
        if user_data is None:
            roles = ["anon"]
            return AuthCredentials(roles), UnauthenticatedUser()
        user_id = user_data.get("user_id")
        roles = ['authenticated']
        # SimpleUser sets user_id as username attribute
        return AuthCredentials(roles), SimpleUser(user_id)
