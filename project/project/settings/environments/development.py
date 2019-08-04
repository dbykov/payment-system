from env import env

db_config = env.db(
        'PAYSYS_DJANGO_DATABASE_URL',
        default='pgsql://payment:payment@localhost:5432/payment',
        engine='django.db.backends.postgresql')

DATABASES = {
    'default': {
        **db_config,
    }
}
