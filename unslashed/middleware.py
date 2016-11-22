import re
from django.conf import settings
from django.core import urlresolvers
from django.http import HttpResponsePermanentRedirect as UnslashedRedirect
from django.utils import six
from django.utils.http import urlquote

if getattr(settings, 'UNSLASHED_USE_302_REDIRECT', None):
    from django.http import HttpResponseRedirect as UnslashedRedirect

trailing_slash_regexp = re.compile(r'(\/(?=\?))|(\/$)')


class RemoveSlashMiddleware(object):
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

    Using this middlware with REMOVE_SLASH set to False or without REMOVE_SLASH
    set means it will do nothing.

    Orginally, based closely on Django's APPEND_SLASH CommonMiddleware
    implementation at
    https://github.com/django/django/blob/master/django/middleware/common.py.
    It has been reworked to use regular expressions instead of deconstructing/
    reconstructing the URL, which was problematically re-encoding some of the
    characters.
    """

    def should_redirect_without_slash(self, request):
        """
        Return True if settings.APPEND_SLASH is True and appending a slash to
        the request path turns an invalid path into a valid one.
        """
        if getattr(settings, 'REMOVE_SLASH', False) and trailing_slash_regexp.search(request.get_full_path()):
            urlconf = getattr(request, 'urlconf', None)
            return (not urlresolvers.is_valid_path(request.path_info, urlconf) and urlresolvers.is_valid_path(
                request.path_info[:-1], urlconf))
        return False

    def get_full_path_without_slash(self, request):
        """
        Return the full path of the request with a trailing slash appended.
        Raise a RuntimeError if settings.DEBUG is True and request.method is
        POST, PUT, or PATCH.
        """
        newurl = "%s://%s%s" % (
            request.scheme,
            request.get_host(), urlquote(request.path[:-1]))
        if request.META.get('QUERY_STRING', ''):
            if six.PY3:
                newurl += '?' + request.META['QUERY_STRING']
            else:
                # `query_string` is a bytestring. Appending it to the unicode
                # string `newurl` will fail if it isn't ASCII-only. This isn't
                # allowed; only broken software generates such query strings.
                # Better drop the invalid query string than crash (#15152).
                try:
                    newurl += '?' + request.META['QUERY_STRING'].decode()
                except UnicodeDecodeError:
                    pass

        if settings.DEBUG and request.method in ('POST', 'PUT', 'PATCH'):
            raise RuntimeError("You called this URL via %(method)s, but the URL doesn't end "
                               "in a slash and you have APPEND_SLASH set. Django can't "
                               "redirect to the slash URL while maintaining %(method)s data. "
                               "Change your form to point to %(url)s (note the trailing "
                               "slash), or set APPEND_SLASH=False in your Django settings." % {'method': request.method,
                                   'url': request.get_host() + new_path,})
        return newurl

    def get_full_path_with_slash(self, request):
        """
        Return the full path of the request with a trailing slash appended.
        Raise a RuntimeError if settings.DEBUG is True and request.method is
        POST, PUT, or PATCH.
        """
        newurl = "%s://%s%s" % (
            request.scheme,
            request.get_host(), urlquote(request.path))
        newurl += '/'
        if request.META.get('QUERY_STRING', ''):
            if six.PY3:
                newurl += '?' + request.META['QUERY_STRING']
            else:
                # `query_string` is a bytestring. Appending it to the unicode
                # string `newurl` will fail if it isn't ASCII-only. This isn't
                # allowed; only broken software generates such query strings.
                # Better drop the invalid query string than crash (#15152).
                try:
                    newurl += '?' + request.META['QUERY_STRING'].decode()
                except UnicodeDecodeError:
                    pass

        if settings.DEBUG and request.method in ('POST', 'PUT', 'PATCH'):
            raise RuntimeError("You called this URL via %(method)s, but the URL doesn't end "
                               "in a slash and you have APPEND_SLASH set. Django can't "
                               "redirect to the slash URL while maintaining %(method)s data. "
                               "Change your form to point to %(url)s (note the trailing "
                               "slash), or set APPEND_SLASH=False in your Django settings." % {'method': request.method,
                                   'url': request.get_host() + new_path,})
        return newurl

    def process_response(self, request, response):
        """
        redirects to the current URL without the trailing slash if settings.REMOVE_SLASH is True
        and our current response's status_code would be a 404
        """
        # If the given URL is "Not Found", then check if we should redirect to
        # a path without a slash appended.
        if response.status_code == 404:
            path = request.path
            whitelists = ['/admin']
            if hasattr(settings, 'UNSLASHED_WHITELIST_STARTSWITH'):
                whitelists += settings.UNSLASHED_WHITELIST_STARTSWITH
            if any(path.startswith(x) for x in whitelists) and not path.endswith('/'):
                return UnslashedRedirect(self.get_full_path_with_slash(request))
            elif self.should_redirect_without_slash(request):
                return UnslashedRedirect(self.get_full_path_without_slash(request))

        return response
