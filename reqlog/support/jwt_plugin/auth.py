# -*- coding: utf-8 -*-
"""`bottle_jwt.auth` module.

Main auth providers class implementation.
"""

from __future__ import print_function
from __future__ import unicode_literals

import collections
import datetime
import logging

import bottle

from bottle import HTTPResponse
import jwt

from .compat import b
from .compat import signature
from .error import JWTAuthError, JWTBackendError, JWTForbiddenError, JWTUnauthorizedError


try:
    import ujson as json

except ImportError:
    try:
        import simplejson as json

    except ImportError:
        import json


logger = logging.getLogger(__name__)


auth_fields = collections.namedtuple("AuthField", "user_id, password")


def jwt_auth_required(callable_obj):
    """A decorator that signs a callable object with an "auth_required"
    attribute (True). We use this attribute to find which handler callbacks
    require an authorized for protected access.

    Args:
        callable_obj (instance): A handler callable object.

    Returns:
        The callable object.
    """
    setattr(callable_obj, "auth_required", True)

    return callable_obj


def jwt_soft_auth_check_required(callable_obj):
    setattr(callable_obj, "auth_soft_check_required", True)

    return callable_obj


class JWTProvider(object):
    """JWT Auth provider concrete class.
    """

    def __init__(
            self,
            fields,
            backend,
            secret,
            id_field="id",
            add_cookie=False,
            cookie_secret=None,
            cookie_path = "/",
            algorithm="HS256",
            ttl=None,
            auth_redirect_rule=None,
            auth_redirect_to=None,
            soft_authentication_keyword=None,
            on_jwt_exception=None,
            on_auth_redirect=None,
            token_recreate_before=None
    ):
        # if not isinstance(backend, BaseAuthBackend):  # pragma: no cover
        #     raise TypeError("backend instance does not implement {} interface".format(BaseAuthBackend))

        self.id_field = id_field
        self.user_field = auth_fields(*fields)
        self.secret = secret
        self.backend = backend
        self.algorithm = algorithm
        self.ttl = ttl

        self.add_cookie = add_cookie
        self.cookie_secret = cookie_secret
        self.cookie_path = cookie_path

        self.auth_redirect_rule = auth_redirect_rule
        self.auth_redirect_to = auth_redirect_to
        self.soft_authentication_keyword = soft_authentication_keyword
        self.on_jwt_exception = on_jwt_exception
        self.on_auth_redirect = on_auth_redirect
        self.token_recreate_before = token_recreate_before

    @property
    def expires(self):
        """Computes the token expiration time based on `self.ttl` attribute.
        """
        return datetime.datetime.utcnow() + datetime.timedelta(
            seconds=self.ttl
        )

    def create_token(self, user):
        """Creates a new signed JWT-valid token.

        Args:
            user (dict): The user record in key/value mapping from instance backend.

        Returns:
            A valid JWT with expiration signature
        """

        if self.id_field not in user:
            raise Exception("Token can't be crated: no '{}' field provided by backend".format(self.id_field))

        payload = user

        if self.ttl:
            payload["exp"] = self.expires

        logger.debug("Token created for payload: {}".format(str(payload)))

        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def validate_token(self, token=""):
        """Validate JWT token.

        Args:
            token (str): A Json Web token string.

        Returns:
            The decrypted token data (dict)

        Raises:
            JWTProviderError, if no token is provided, or if it is expired.
        """
        if not token:
            logger.debug("Forbidden access")
            raise JWTForbiddenError("Cannot access this resource!")

        try:
            decoded = jwt.decode(
                token.split(" ", 1).pop(),
                self.secret,
                algorithms=self.algorithm
            )

            logger.debug("Token validation passed: {}".format(token))

            user_uid = decoded.get(self.id_field)

            bottle.request.environ["jwt_payload"] = decoded
            if "scope" in decoded:
                bottle.request.environ["jwt_scope"] = decoded["scope"]
            bottle.request.environ["jwt_user_id"] = user_uid
            bottle.request.environ["jwt_authenticated"] = True

            if not user_uid:  # pragma: no cover
                raise JWTUnauthorizedError("Invalid User token")

            user = self.backend.get_user(user_uid)

            if user:
                return user

            raise JWTUnauthorizedError("Invalid User token")

        except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
            logger.debug("{}: {}".format(e.args[0], token))
            raise JWTUnauthorizedError("Invalid auth token provided.")

    def authenticate(self, request):
        """Returns a valid JWT for provided credentials.

        Args:
            request (instance): bottle.request instance.

        Returns:
            A JWT token string.

        Raises:
            BackendError, if an auth backend error occurs.
            JWTProviderError,, if user can't be authorized.
        """
        if request.content_type.startswith("application/json"):  # pragma: no cover
            try:
                username = request.json.get(self.user_field.user_id)
                password = request.json.get(self.user_field.password)
            except (AttributeError, json.decoder.JSONDecodeError):
                raise JWTAuthError("Unable to authenticate User")

        else:
            username = request.forms.get(self.user_field.user_id)
            password = request.forms.get(self.user_field.password)

        user = self.backend.authenticate_user(username, password)

        if user:
            return self.create_token(user), user

        raise JWTAuthError("Unable to authenticate User")

    def authorize(self, request):
        """Checks if incoming request is authenticated.

        Args:
            request (instance): bottle.request instance.

        Returns:
            Request JWT decrypted payload, if request is authenticated else
            False.

        Raises:
            JWTProvider, if no auth header if present or invalid/expired
            token is provided.
        """
        user_token = request.get_header("Authorization", "")

        if len(user_token) == 0:
            user_token = request.get_cookie("Authorization", secret=self.cookie_secret)

        return self.validate_token(user_token) or False


class JWTProviderPlugin(object):
    """A `bottle.Bottle` application plugin for JWTProvider.

    Attributes:
        keyword (str): The string keyword for application registry.
        provider (instance): A JWTProvider instance.
        login_enable (bool): If True app is mounted with a login handler.
        auth_endpoint (str): The authentication uri for provider if
                             login_enabled is True.
        kwargs : JWTProvider init parameters.
    """
    scope = ("plugin", "middleware")
    api = 2

    def __init__(self, keyword, auth_endpoint, login_enable=True, scope="plugin", **kwargs):
        self.keyword = keyword
        self.login_enable = login_enable
        self.scope = scope
        self.provider = JWTProvider(**kwargs)
        self.auth_endpoint = auth_endpoint

    @staticmethod
    def get_redirect_response_object(url, code=None):
        if not code:
            code = 303 if bottle.request.get("SERVER_PROTOCOL") == "HTTP/1.1" else 302

        res = bottle.response.copy(cls=HTTPResponse)
        res.status = code
        res.body = ""
        res.set_header("Location", bottle.urljoin(bottle.request.url, url))

        return res

    def get_resp_for_auth_cookie_erase(self, redirect_to):
        response = JWTProviderPlugin.get_redirect_response_object(redirect_to)

        response.set_cookie(
            "Authorization",
            "",
            max_age=self.provider.ttl,
            path=self.provider.cookie_path,
            secret=self.provider.cookie_secret
        )

        return response

    def is_authenticated(self):
        if "jwt_user_id" in bottle.request.environ:
            return True

    def setup(self, app):  # pragma: no cover # noqa: C901 # (too complex)
        """Make sure that other installed plugins don't affect the same
        keyword argument and check if metadata is available.
        """

        if self.login_enable:
            #  Route a login handler in bottle.py app instance.
            @app.post(self.auth_endpoint)
            def auth_handler():
                try:
                    token, payload = self.provider.authenticate(bottle.request)
                    string_token = token.decode("utf-8")

                    if (self.provider.auth_redirect_rule is not None) and self.provider.auth_redirect_rule():
                        response = self.get_redirect_response_object(self.provider.auth_redirect_to)

                        if self.provider.on_auth_redirect:
                            response = self.provider.on_auth_redirect(response)

                    else:
                        json_payload = {
                            "access_token": string_token,
                            "scope": payload["scope"],
                            "token_type": "bearer",
                            "expires_in": self.provider.ttl
                        }

                        response_headers = {
                            "Authorization": "Bearer " + string_token,
                            "Authorization-Scope": payload["scope"],
                            "Authorization-Token-Type": "bearer",
                            "Authorization-Expires-In": self.provider.ttl
                        }

                        response = HTTPResponse(status=200, body=json_payload, headers=response_headers)

                    response.set_cookie(
                        "Authorization",
                        "Bearer " + string_token,
                        max_age=self.provider.ttl,
                        path=self.provider.cookie_path,
                        secret=self.provider.cookie_secret
                    )

                    return response

                except JWTAuthError as error:
                    return {"AuthError": error.args[0]}

                except JWTBackendError:
                    return {"AuthBackendError": "Try later or contact admin!"}

        for other in app.plugins:
            if not isinstance(other, JWTProviderPlugin):
                continue

            if other.keyword == self.keyword:
                raise bottle.PluginError("Found another JWT plugin "
                                         "with conflicting settings ("
                                         "non-unique keyword).")

    @staticmethod
    def _is_authenticated():
        if "jwt_authenticated" not in bottle.request.environ:
            return False

        return bottle.request.environ["jwt_authenticated"]

    def apply(self, callback, context):  # pragma: no cover  # noqa: C901 #(too complex)

        """Implement bottle.py API version 2 `apply` method.
        """

        _signature = signature(callback).parameters

        def injected(*args, **kwargs):
            if self.keyword in _signature:
                kwargs[self.keyword] = self.provider

            if self.provider.soft_authentication_keyword in _signature:
                kwargs[self.provider.soft_authentication_keyword] = self._is_authenticated()

            return callback(*args, **kwargs)

        def soft_check_wrapper(*args, **kwargs):
            try:
                user = self.provider.authorize(bottle.request)

                if user:
                    authorized = True
                else:
                    authorized = False

                bottle.request.environ["jwt_authenticated"] = authorized
                setattr(bottle.request, "get_user", lambda _: user)
                return injected(*args, **kwargs)

            except JWTUnauthorizedError as _:
                pass

            except JWTForbiddenError as _:
                pass

            except JWTBackendError:
                pass

            bottle.request.environ["jwt_authenticated"] = False
            return injected(*args, **kwargs)

        def wrapper(*args, **kwargs):
            # if self.provider.on_jwt_exception is not None:

            try:
                user = self.provider.authorize(bottle.request)
                setattr(bottle.request, "get_user", lambda _: user)

                needful_scopes = self._get_route_scopes(context)
                if len(needful_scopes):
                    if not self._is_access_allowed(needful_scopes):
                        raise JWTForbiddenError()

                if self.provider.add_cookie and (self.provider.token_recreate_before is not None):
                    exp = bottle.request.environ["jwt_payload"]["exp"]

                    d = (datetime.datetime.utcfromtimestamp(exp) - datetime.datetime.utcnow())
                    if d.total_seconds() <= self.provider.token_recreate_before:
                        token = self.provider.create_token(bottle.request.environ["jwt_payload"])
                        string_token = token.decode("utf-8")

                        bottle.response.set_cookie(
                            "Authorization",
                            "Bearer " + string_token,
                            max_age=self.provider.ttl,
                            path=self.provider.cookie_path,
                            secret=self.provider.cookie_secret
                        )

                return injected(*args, **kwargs)

            except JWTUnauthorizedError as error:
                if self.provider.on_jwt_exception:
                    r = self.provider.on_jwt_exception()
                    if r:
                        return r

                bottle.response.content_type = b("application/json")
                bottle.response._status_line = b("401 Unauthorized")
                return {"AuthError": error.args}

            except JWTForbiddenError as error:
                r = self.provider.on_jwt_exception()
                if r:
                    return r

                bottle.response.content_type = b("application/json")
                bottle.response._status_line = b("403 Forbidden")
                return {"AuthError": error.args}

            except JWTBackendError:
                r = self.provider.on_jwt_exception()
                if r:
                    return r

                bottle.response.content_type = b("application/json")
                bottle.response._status_line = b("503 Service Unavailable")
                return {"AuthBackendException": "Try later or contact admin!"}

        if self.scope == "middleware":
            logger.debug("JWT Authentication: {}".format(context.rule))

            return wrapper

        if hasattr(callback, "auth_soft_check_required") and (not hasattr(callback, "auth_required")):
            return soft_check_wrapper

        if not hasattr(callback, "auth_required"):
            return injected

        logger.debug("JWT Authentication: {}".format(context.rule))
        return wrapper

    @staticmethod
    def _is_access_allowed(needful_scopes):
        if not len(needful_scopes):
            return True

        avail_scopes = JWTProviderPlugin._get_avail_scopes()
        if not len(avail_scopes):
            return False

        access_granted = True
        for scope in needful_scopes:
            if scope not in avail_scopes:
                access_granted = False
                break

        return access_granted

    @staticmethod
    def _get_route_scopes(context):
        config = context.config

        if "scopes" not in config:
            return []

        return config["scopes"]

    @staticmethod
    def _get_avail_scopes():  # pragma: no coverage # this function will be mocked for each test
        if "jwt_scope" not in bottle.request.environ:
            raise []

        return bottle.request.environ["jwt_scope"]
