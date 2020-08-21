import pytest
from django.conf import settings


@pytest.mark.trylast
def pytest_configure(config):
    config.addinivalue_line("markers", "longrun: mark test as slow")

    if not config.option.longrun:
        setattr(config.option, 'markexpr', 'not longrun')

    settings.configure(
        SECRET_KEY='testing',

        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            },
        },

        FFLAG_CACHE_NAME='default',

    )


def pytest_addoption(parser):
    parser.addoption('--longrun', action='store_true', dest="longrun",
                     default=False, help="enable long running tests")
