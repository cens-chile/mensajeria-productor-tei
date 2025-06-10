from rest_framework_simplejwt.authentication import JWTAuthentication, AUTH_HEADER_TYPE_BYTES
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _


def get_from_cookie(cookie):
    parts_list = cookie.split('; ')
    cookie_dict = {}
    for part in parts_list:
        part_list = part.split('=', 1)
        cookie_dict[part_list[0]] = part_list[1]
    return cookie_dict


class JWTCookieAuthentication(JWTAuthentication):

    @staticmethod
    def get_access_from_cookie(cookie):
        cookie_dict = get_from_cookie(cookie)
        if 'access' in cookie_dict:
            return cookie_dict['access']
        return None

    @staticmethod
    def get_refresh_from_cookie(cookie):
        cookie_dict = get_from_cookie(cookie)
        if 'refresh' in cookie_dict:
            return cookie_dict['refresh']
        return None

    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get('HTTP_COOKIE')
        if header is None:
            return None
        header = self.get_access_from_cookie(header)

        if isinstance(header, str):
            # Work around django test client oddness

            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "COOKIE"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if len(parts) != 1:
            raise AuthenticationFailed(
                _('Authorization cookie must contain a value'),
                code='bad_authorization_header',
            )

        return parts[0]
