from pathlib import Path
from dotenv import load_dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#Collecting StaticFiles
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Ensures STATIC_URL is also configured correctly
STATIC_URL = '/static/'

# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
SECRET_KEY = "your_secret_key_here"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'djangogram-pet-projec.lm.r.appspot.com',
    'localhost',
    '127.0.0.1',
    '127.0.0.1:8000',
    '*',
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "posts",
    'allauth',  # Integrating third party authentification
    'django.contrib.sites',
    'storages',     #Specific for deployment on Gcloud to store data
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "accounts.middleware.EnsureProfileMiddleware",
]

SESSION_ENGINE = "django.contrib.sessions.backends.db"  # debugging login_view

ROOT_URLCONF = "DjangoGram.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "DjangoGram.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# # Database configuration for deployment on Gcloud
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'django_gramm_db',
#         'USER': 'postgres',
#         'PASSWORD': 'your_password',
#         # 'HOST': '34.118.55.166', #This host to be used during local testing and migrations
#         'HOST': '/cloudsql/djangogram-pet-projec:europe-central2:djangogramdb',
#         # 'PORT': '5432',
#     }
# }

# Database configuration for deployment locally
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_gramm_db',
        'USER': 'django_gramm_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Used for django.contrib.
# required for the sites framework to
# function correctly
SITE_ID = 1

# Email handiling, do not run debug in production

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your_mail'
EMAIL_HOST_PASSWORD = "your_password"
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Media files config
# MEDIA_URL = '/media/' #for local deployment
MEDIA_ROOT = BASE_DIR / 'media'

#For Gcloud Functionality need to include this:
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'djangogram-pet-projec.appspot.com'
GS_DEFAULT_ACL = 'publicRead'  # Or any other appropriate ACL

MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_URL = "/static/"

# django-allauth settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = '/accounts/profile/update/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'none'  # For standard accounts

SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'  # Disable for social accounts


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    },
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
        'USER_FIELDS': ['id', 'login', 'name', 'email'],
    }
}

