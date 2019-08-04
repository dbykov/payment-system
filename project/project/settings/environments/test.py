from env import env

dbconfig = env.db(
    'PAYSYS_DJANGO_TEST_DATABASE_URL',
    default='pgsql://test:test@localhost:5432/test',
    engine='django.db.backends.postgresql')


DATABASES = {
    'default': {
        **dbconfig,
        'TEST': {'NAME': dbconfig['NAME']},
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
