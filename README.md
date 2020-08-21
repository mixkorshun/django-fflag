# django-fflag

[![Build Status](https://travis-ci.org/mixkorshun/django-fflag.svg?branch=master)](https://travis-ci.org/mixkorshun/django-fflag)
[![codecov](https://codecov.io/gh/mixkorshun/django-fflag/branch/master/graph/badge.svg)](https://codecov.io/gh/mixkorshun/django-fflag)

Lightweight feature flag for django.

Feature flag is useful technique to develop your software. When you implement new functionality in you project,
you probably want to enable it gradually for some users.

django-fflags is realization of feature flag mechanism with following benefits:
 - flags can be enabled to some part of your users or concrete users list
 - flags part will be different and depends on your flag name
 - it will works with any users count

Learn more about feature flags: https://www.martinfowler.com/articles/feature-toggles.html

## Installation

Install package:
```bash
pip install django-fflag
```

Add following configuration to `settings.py`:

```python

INSTALLED_APPS = (
    ...,
    "fflag",
)

MIDDLEWARE = (
    ...,
    "django.contrib.auth", # FFlagMiddleware uses request.user.id
    "django.contrib.sessions", # FFlagMiddleware uses request.session to store unauthenticated client id
    ...,
    "fflags.middleware.FFlagMiddleware",
)

# Persistent cache storage strongly recommended for feature-flags.
# You can configure custom persistent cache using following config:

FFLAG_CACHE_NAME = "fflag"

CACHES = {
    ...,
    "fflag": {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'NAME': 'fflag_flags',
    }
}
```

## Usage

When you write new code, you may wrap it with following if:
```python
if request.fflag_enabled("my_new_feature"):
    ...
```

or without request:
```python
if fflag_enabled(uniq_client_id, "my_new_feature"):
    ...
```

That means that your code will be not executed until feature flag is enabled.

To manage feature flags you may use following management commands:

 - **manage.py fflag_list** - print list of used feature flags. 
 - **manage.py fflag_list_enabled_for** - print list enabled feature flags for specified id (usually user id).
 - **manage.py fflag_get** - print information for specified feature flag.
 - **manage.py fflag_set_part** - set feature flag enable part. For example 0.4 will enable functionality for ~40% of users.
 - **manage.py fflag_add_part_ids** - extend feature flag part enabled ids (usually user ids)
 - **manage.py fflag_set_part_ids** - override feature flag part enabled ids (usually user ids)


**IMPORTANT NOTE**: Feature flag will be invisible by management commands after `fflag_enabled` function will be called.
