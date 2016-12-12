import re
from django.conf import settings
from django.core import urlresolvers
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils.encoding import iri_to_uri
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # pragma: no cover
    MiddlewareMixin = object  # Django<1.10


trailing_slash_regexp = re.compile(r'(\/(?=\?))|(\/$)')


class RemoveSlashMiddleware(MiddlewareMixin):
    """
    This middleware provides the inverse of the APPEND_SLASH option built into
    django.middleware.common.CommonMiddleware. It should be placed just before
    or just after CommonMiddleware.

    If REMOVE_SLASH is True, the initial URL ends with a slash, and it is not
    found in the URLconf, then a new URL is formed by removing the slash at the
    end. If this new URL is found in the URLconf, then Django redirects the
    request to this new URL. Otherwise, the initial URL is processed as usual.

    For example, foo.com/bar/ will be redirected to foo.com/bar if you don't
    have a valid URL pattern for foo.com/bar/ but do have a valid pattern for
    foo.com/bar.

    Using this middleware with REMOVE_SLASH set to False or without
    REMOVE_SLASH set means it will do nothing.

    Originally, based closely on Django's APPEND_SLASH CommonMiddleware
    implementation at
    https://github.com/django/django/blob/master/django/middleware/common.py.
    It has been reworked to use regular expressions instead of deconstructing/
    reconstructing the URL, which was problematically re-encoding some of the
    characters.
    """

    def __init__(self, *args, **kwargs):
        if not getattr(settings, 'REMOVE_SLASH', False):
            raise MiddlewareNotUsed()
        self.response_class = HttpResponsePermanentRedirect
        if getattr(settings, 'UNSLASHED_USE_302_REDIRECT', None):
            self.response_class = HttpResponseRedirect
        super(RemoveSlashMiddleware, self).__init__(*args, **kwargs)

    def should_redirect_without_slash(self, request):
        """
        Return True if appending a slash to
        the request path turns an invalid path into a valid one.
        """
        if trailing_slash_regexp.search(request.get_full_path()):
            urlconf = getattr(request, 'urlconf', None)

            return (
                not urlresolvers.is_valid_path(request.path_info, urlconf) and
                urlresolvers.is_valid_path(request.path_info[:-1], urlconf))
        return False

    def get_full_path_without_slash(self, request):
        """
        Return the full path of the request without a trailing slash appended.

        Raise a RuntimeError if settings.DEBUG is True and request.method is
        POST, PUT, or PATCH.
        """
        path = request.path
        if path.endswith('/'):
            path = path[:-1]
        new_path = '{}{}'.format(
            path,
            ('?' + iri_to_uri(request.META.get('QUERY_STRING', '')))
            if request.META.get('QUERY_STRING', '')
            else ''
        )
        if settings.DEBUG and request.method in ('POST', 'PUT', 'PATCH'):
            raise RuntimeError(
                "You called this URL via %(method)s, but the URL ends "
                "in a slash and you have REMOVE_SLASH set. Django-unslashed "
                "can't redirect to the slash URL while maintaining %(method)s "
                "data. Change your form to point to %(url)s (note there is no"
                "trailing slash), or set REMOVE_SLASH=False in your Django "
                " settings." % {
                    'method': request.method,
                    'url': request.get_host() + new_path,
                }
            )
        return new_path

    def process_response(self, request, response):
        """
        Redirects to the current URL without the trailing slash if
        settings.REMOVE_SLASH is True and our current response's
        status_code would be a 404
        """
        # If the given URL is "Not Found", then check if we should redirect to
        # a path without a slash appended.
        if response.status_code == 404:
            path = request.path
            whitelists = getattr(settings,
                                 'UNSLASHED_WHITELIST_STARTSWITH',
                                 ['/admin'])
            if any(path.startswith(x) for x in whitelists):
                return response
            if self.should_redirect_without_slash(request):
                return self.response_class(
                    self.get_full_path_without_slash(request))
        return response
