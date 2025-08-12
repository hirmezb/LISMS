"""
Custom authentication backend for Auth0 JWTs.

This module defines a DRF ``BaseAuthentication`` class that validates
JSON Web Tokens (JWTs) issued by Auth0.  The class relies on the
``python-jose`` package to decode and verify the token signature.  If a
valid token is present in the ``Authorization`` header of the request it
returns an anonymous user along with the token payload; otherwise it
returns ``None`` to allow other authentication backends (e.g.
SessionAuthentication) to attempt authentication.
"""

from __future__ import annotations

import json
from urllib.request import urlopen

from django.conf import settings
from rest_framework import authentication, exceptions

try:
    # ``python-jose`` is required to decode Auth0 JWTs.
    from jose import jwt  # type: ignore
except Exception as exc:  # pragma: no cover
    jwt = None  # type: ignore


class Auth0JWTAuthentication(authentication.BaseAuthentication):
    """Authenticates requests using an Auth0-issued JWT.

    The expected format of the ``Authorization`` header is ``Bearer <token>``.
    If no header is present or the token cannot be validated, this backend
    returns ``None`` so that other backends may continue the authentication
    process.  If the token is invalid an ``AuthenticationFailed`` exception
    is raised.
    """

    def authenticate(self, request):  # type: ignore[override]
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        parts = auth_header.split()
        if parts[0].lower() != "bearer" or len(parts) != 2:
            return None
        token = parts[1]
        if jwt is None:
            raise exceptions.AuthenticationFailed(
                "python-jose is not installed; cannot validate JWT."
            )
        try:
            # Fetch the signing keys from Auth0.  The JWKS endpoint returns
            # a set of keys that can be used to verify the JWT signature.
            jsonurl = urlopen(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
            jwks = json.loads(jsonurl.read())
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = None
            for key in jwks.get("keys", []):
                if key.get("kid") == unverified_header.get("kid"):
                    rsa_key = {
                        "kty": key.get("kty"),
                        "kid": key.get("kid"),
                        "use": key.get("use"),
                        "n": key.get("n"),
                        "e": key.get("e"),
                    }
                    break
            if rsa_key is None:
                raise exceptions.AuthenticationFailed("Unable to find appropriate key")
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=settings.AUTH0_ALGORITHMS,
                audience=settings.AUTH0_API_AUDIENCE,
                issuer=f"https://{settings.AUTH0_DOMAIN}/",
            )
        except Exception as exc:
            raise exceptions.AuthenticationFailed(f"Unauthenticated: {exc}")
        # At this point the token is valid.  Since Auth0 stores user
        # information in the token, you could look up a corresponding
        # ``UserAccount`` instance here or create one on the fly.  For
        # simplicity we return ``None`` as the user and the payload for the
        # authentication credentials.  Downstream view code can access
        # ``request.auth`` to examine token claims if necessary.
        return (None, payload)

    def authenticate_header(self, request):  # type: ignore[override]
        return "Bearer"