import environ
import sys

root = environ.Path(__file__) - 3
environ.Env.read_env()  # reading .env file
default_env = 'test' if sys.argv[1:2] == ['test'] else 'production'
env = environ.Env(PAYSYS_DJANGO_ENV=(str, default_env))
