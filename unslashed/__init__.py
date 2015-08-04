__version__ = '0.3.0'

from django.conf import settings
from django.http import HttpResponsePermanentRedirect as UnslashedRedirect

if getattr(settings, 'UNSLASHED_USE_302_REDIRECT', None):
    from django.http import HttpResponseRedirect as UnslashedRedirect
