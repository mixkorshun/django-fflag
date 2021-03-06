from dataclasses import dataclass

import pytest
from django.contrib.sessions.backends.cache import SessionStore
from django.http import HttpResponse
from django.test import RequestFactory

from fflag.middleware import FFlagMiddleware
from fflag.models import fflag_set_part_ids, fflag_set_part


@dataclass
class SimpleUser:
    id: int


@pytest.mark.parametrize('user_id,expected', [(12, True), (11, False)])
def test_fflag_enabled_for_authorized_user(user_id, expected):
    fflag_set_part_ids('fflag_1', [12])

    middleware = FFlagMiddleware(lambda request: HttpResponse(''))

    req = RequestFactory().get('/')
    req.user = SimpleUser(id=user_id)
    middleware(req)

    assert req.fflag_enabled('fflag_1') == expected


@pytest.mark.parametrize('user_id,expected', [(12, True), (11, False)])
def test_fflag_enabled_for_unauthorized_user(user_id, expected):
    fflag_set_part_ids('fflag_1', [12])

    middleware = FFlagMiddleware(lambda request: HttpResponse(''))

    req = RequestFactory().get('/')
    req.session = SessionStore()
    req.session['FFLAG_USER_ID'] = user_id
    middleware(req)

    assert req.fflag_enabled('fflag_1') == expected


def test_fflag_for_new_unauthorized_user():
    fflag_set_part('fflag_1', 1)

    middleware = FFlagMiddleware(lambda request: HttpResponse(''))

    req = RequestFactory().get('/')
    req.session = SessionStore()
    middleware(req)

    assert req.fflag_enabled('fflag_1')
