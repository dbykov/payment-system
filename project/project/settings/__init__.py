"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
Default environment is `developement`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""
from split_settings.tools import include

from env import env

base_settings = [
    'components/*.py',

    # Select the right env:
    'environments/%s.py' % env('PAYSYS_DJANGO_ENV'),
]

# Include settings:
include(*base_settings)
