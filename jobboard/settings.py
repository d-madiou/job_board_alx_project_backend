import os
from datetime import timedelta
from decouple import config, Csv
import dj_database_url
from pathlib import Path

# --------------------
# BASE DIRECTORY
# --------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------
# ENVIRONMENT SETTINGS
# --------------------
ENVIRONMENT = config("ENVIRONMENT", default="development")  # 'development' or 'production'
DEBUG = config("DEBUG", default=True, cast=bool)
SECRET_KEY = config("SECRET_KEY", default="changeme-secret-key")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=Csv())

# --------------------
# INSTALLED APPS
# --------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'corsheaders',

    # Your apps
    'jobs',
    'companies',
    'users',
]

# --------------------
# MIDDLEWARE
# --------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------
# URLS & WSGI
# --------------------
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# --------------------
# DATABASE CONFIGURATION
# --------------------
POSTGRES_LOCALLY = config("POSTGRES_LOCALLY", default=False, cast=bool)

if ENVIRONMENT == "production" and not POSTGRES_LOCALLY:
    # Railway or production mode
    DATABASES = {
        "default": dj_database_url.config(
            default=config("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # Local development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DATABASE_NAME", default="jobboard_db"),
            "USER": config("DATABASE_USER", default="postgres"),
            "PASSWORD": config("DATABASE_PASSWORD", default="postgres"),
            "HOST": config("DATABASE_HOST", default="localhost"),
            "PORT": config("DATABASE_PORT", default="5432"),
        }
    }

# --------------------
# PASSWORD VALIDATORS
# --------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------
# LANGUAGE / TIMEZONE
# --------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --------------------
# STATIC & MEDIA FILES
# --------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --------------------
# CORS SETTINGS
# --------------------
CORS_ALLOW_ALL_ORIGINS = True

# --------------------
# REST FRAMEWORK SETTINGS
# --------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}

# --------------------
# SIMPLE JWT SETTINGS
# --------------------
JWT_SECRET_KEY = config("JWT_SECRET_KEY", default="supersecretjwtkey")
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SIGNING_KEY": JWT_SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# --------------------
# DEFAULT PRIMARY KEY
# --------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
