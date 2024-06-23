"""
Django base settings for project to build other settings files upon.
"""

import environ

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('app_django')

env = environ.Env()

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-b*00ozwhih)h2qz5ti$vq*e*sv5^!n_s)h&^a#x#$^q5-z$apb')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', False)

# Users & Authentication
AUTH_USER_MODEL = 'users.User'

# Update backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'app_django.users.backends.EmailBackend',  # Add your custom backend here
)

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]
THIRD_PARTY_APPS = []
LOCAL_APPS = [
    'users',
    'cars'
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

THIRD_PARTY_MIDDLEWARE = []
DJANGO_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
MIDDLEWARE = THIRD_PARTY_MIDDLEWARE + DJANGO_MIDDLEWARE

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database

DATABASES = {
    'default': env.db('DATABASE_URL'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# Passwords hashers

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.ScryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

TIME_ZONE = 'America/Lima'
LANGUAGE_CODE = 'es'
SITE_ID = 1
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    str(APPS_DIR('static')),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media
MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_URL = '/media/'

# Login
# LOGIN_URL = '/login/'
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = LOGIN_URL

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin
ADMIN_URL = 'admin/'
ADMINS = [
    ("""Jose Garayar""", 'jgarayarp@uni.pe'),
]
MANAGERS = ADMINS

# Security
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')