This app uses Django server-side sessions, not JWT.

After Google SSO succeeds:

1. Google redirects to `/api/v1/auth/google/callback`.
2. `django-allauth` validates Google’s OAuth response, creates/updates the local `User`, and calls Django login.
3. Django creates a server-side session (normally stored in the database) and sends the browser a `sessionid` cookie.
4. The browser automatically includes that cookie on later API calls when the frontend uses `credentials: "include"`—which it does for `/auth/me` and logout.

For every later request Django authenticates it like this:

```text
Browser request
  Cookie: sessionid=<opaque random id>
       ↓
SessionMiddleware loads the server-side session
       ↓
AuthenticationMiddleware sets request.user
       ↓
DRF SessionAuthentication accepts request.user
       ↓
IsAuthenticated permits the endpoint
```

The important project settings are in [base.py](config/settings/base.py):

- `DEFAULT_AUTHENTICATION_CLASSES = SessionAuthentication`
- `DEFAULT_PERMISSION_CLASSES = IsAuthenticated`
- `SESSION_COOKIE_HTTPONLY = True` means frontend JavaScript cannot read or steal the session cookie directly.
- `CORS_ALLOW_CREDENTIALS = True` allows the browser to attach the cookie to permitted cross-origin frontend requests.

The frontend’s call is here: [auth.ts](../ui/lib/auth.ts)

```ts
fetch(authUrls.me, { credentials: "include" });
```

`GET /api/v1/auth/me` then checks `request.user.is_authenticated` in [views.py](apps/accounts/views.py). You do not manually pass a JWT or Google access token to that endpoint.

For state-changing calls (`POST`, `PATCH`, `DELETE`), session auth also requires CSRF protection. Your `/me` endpoint returns a CSRF token and the UI sends it back as `X-CSRFToken` on logout, which is the right pattern.

Google’s own OAuth token is used by the backend during sign-in; it is not the credential used to authenticate the user’s subsequent calls to your API.
