from env import env

db_config = env.db(
        'PAYSYS_DJANGO_DATABASE_URL',
        engine='django.db.backends.postgresql')

DATABASES = {
    'default': {
        **db_config,
    }
}

