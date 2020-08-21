from django.core.exceptions import ImproperlyConfigured
from django.utils.timezone import now

from .models import fflag_enabled


def fflag_enabled_method(self, flag: str, _id: int = None):
    if _id is None:
        _id = self.user.id if hasattr(self, 'user') else None

        # anonymous user, or user backend not specified
        if _id is None:
            if not hasattr(self, 'session'):
                raise ImproperlyConfigured(
                    'SessionMiddleware is required to use `fflag_enabled` function without `id` argument.'
                )

            # get user id from session
            _id = self.session.get('FFLAG_USER_ID')
            if not _id:
                # or write it to session
                _id = int(now().timestamp())
                self.session['FFLAG_USER_ID'] = _id
                self.session.save()

    return fflag_enabled(_id, flag)


class FFlagMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        fflag_enabled_bound_method = fflag_enabled_method.__get__(request, request.__class__)
        setattr(request, 'fflag_enabled', fflag_enabled_bound_method)
        return self.get_response(request)
