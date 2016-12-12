# django-unslashed

[![CircleCI](https://circleci.com/gh/frnhr/django-unslashed/tree/master.svg?style=shield)](https://circleci.com/gh/frnhr/django-unslashed/tree/master)
[![codecov](https://codecov.io/gh/frnhr/django-unslashed/branch/master/graph/badge.svg)](https://codecov.io/gh/frnhr/django-unslashed)

This middleware provides the inverse of the Django CommonMiddleware `APPEND_SLASH` feature. It can automatically remove trailing URL slashes and 301 redirect to the non-slash-terminated URL. This behavior is performed if the initial URL ends in a slash and is invalid, removing the trailing slash produces a valid URL, and `REMOVE_SLASH` is set to True. Otherwise there is no effect.

For example, foo.com/bar/ will be redirected to foo.com/bar if you don't have a valid URL pattern for foo.com/bar/ but do have a valid pattern for foo.com/bar and `REMOVE_SLASH=True`.


## Fork info

This is a fork from https://github.com/harshvb7/django-unslashed, which is in turn a fork of https://github.com/dghubble/django-unslashed.

Changes to this fork:
    * updated for Django 1.10, compatible down to 1.8, and Python 2.7, 3.3-3.5.
    * PyPI package name with prefix `tocka-`
    * Added CircleCI and Codecov, removed TravisCI    


## Install

To install `django-unslashed`,

```
pip install tocka-django-unslashed
```

If you're using a `requirements.txt` file, add `django-unslashed>=0.3.0` to it.


## Usage

Modify your Django `settings.py` file to add `unslashed.middleware.RemoveSlashMiddleware`
to your `MIDDLEWARE_CLASSES` just before or after `django.middleware.common.CommonMiddleware`.

```python
MIDDLEWARE_CLASSES = (
    # ...
    'unslashed.middleware.RemoveSlashMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ...
)
```

Set `REMOVE_SLASH` to True and `APPEND_SLASH` to False,

```python
APPEND_SLASH = False
REMOVE_SLASH = True
```

If `REMOVE_SLASH` is False or unset, the RemoveSlashMiddleware has no effect.


Set `UNSLASHED_USE_302_REDIRECT` to True if you want to use HttpRedirect instead of HttpPermanentRedirect,

```python
UNSLASHED_USE_302_REDIRECT = True
```

## Rationale

Web applications [should](http://googlewebmastercentral.blogspot.com/2010/04/to-slash-or-not-to-slash.html) have a URL structure which either:

1. Uses trailing slashes and redirects to append slashes if invalid non-slashed-terminated URLs are accessed.
2. Uses no trailing slash URLs and redirects to unslahed URLs if invalid slash terminated URLs are accessed. The prior is the Django default, while the later is possible by adding this middleware to your project.


## Notes

Based closely on Django's APPEND_SLASH CommonMiddleware [implementation](https://github.com/django/django/blob/master/django/middleware/common.py).


## Testing

### Tox

This will run tests on multiple versions of Python and Django, as defined in `tox.ini`.

```bash
$ git clone https://github.com/frnhr/django-unslashed.git
$ cd django-unslashed
$ pip install -r requirements-dev.txt
$ tox
...
...
...
________________________________________________________________________________________________________ summary _________________________________________________________________________________________________________
  django_master-py35: commands succeeded
  django_master-py34: commands succeeded
  django_master-py27: commands succeeded
  django110-py35: commands succeeded
  django110-py34: commands succeeded
  django110-py27: commands succeeded
  django19-py35: commands succeeded
  django19-py34: commands succeeded
  django19-py27: commands succeeded
  django18-py35: commands succeeded
  django18-py34: commands succeeded
  django18-py33: commands succeeded
  django18-py27: commands succeeded
  lint: commands succeeded
  congratulations :)
```


## License

[MIT License](LICENSE)
