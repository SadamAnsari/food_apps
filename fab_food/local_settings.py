import os

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEFAULT_FROM_EMAIL = 'sadamansari22@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sadamansari22@gmail.com'
EMAIL_HOST_PASSWORD = 'hbkjlkaastpmahij'
EMAIL_USE_TLS = True
EMAIL_PORT = 587


