"""
Django settings for lims_project.

This configuration file defines core settings for running the Laboratory
Information and Sample Management System (LISMS) back end.  It uses environment
variables where possible to avoid hardcoding secrets into source control.  If
no environment variables are provided, sensible defaults are used for
development only.  For production, override these values with secure
credentials.
"""

from __future__ import annotations

import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me-please")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in {"1", "true", "yes"}

ALLOWED_HOSTS: list[str] = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")


# Application definition

INSTALLED_APPS = [
    # Third party apps
    "corsheaders",
    "rest_framework",
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local apps
    "lims_app",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "lims_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "lims_project.wsgi.application"


DATABASES = {
    "default": {
        # For development you can switch to SQLite by uncommenting the following
        # lines and removing the MSSQL configuration below.  SQLite requires
        # no external dependencies.  When using SQLite the data will be
        # persisted in ``db.sqlite3`` at the project root.
        #
        # "ENGINE": "django.db.backends.sqlite3",
        # "NAME": BASE_DIR / "db.sqlite3",

        # MSSQL database configuration.  Requires the ``mssql-django`` or
        # ``django-pyodbc-azure`` backend and a compatible ODBC driver.  See
        # README.md for instructions on installing the driver and
        # dependencies.  Fill in your own credentials below.
        "ENGINE": "mssql",
        "NAME": os.environ.get("DB_NAME", "lims_db"),
        "USER": os.environ.get("DB_USER", "your_username"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "your_password"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "1433"),
        "OPTIONS": {
            # Adjust driver version if necessary; ensure the driver is installed on
            # your system.  On Linux systems you can install the Microsoft
            # drivers from packages.microsoft.com.
            "driver": os.environ.get("ODBC_DRIVER", "ODBC Driver 17 for SQL Server"),
        },
    }
}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    # Use Django's standard ``django.contrib.auth`` permissions or override
    # with custom authentication classes to validate JWTs from Auth0.
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "lims_app.authentication.Auth0JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# CORS configuration.  The React front end runs on http://localhost:3000
# during development.  In production adjust this list to your
# deployed domains.
CORS_ALLOWED_ORIGINS = [
    os.environ.get("CORS_ALLOWED_ORIGIN", "http://localhost:3000"),
]

# Auth0 configuration.  Fill these values with your Auth0 domain, API
# audience, and algorithm as configured in the Auth0 dashboard.  The
# ``Auth0JWTAuthentication`` class will reference these values.
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN")
AUTH0_API_AUDIENCE = os.environ.get("AUTH0_API_AUDIENCE", "YOUR_AUTH0_API_AUDIENCE")
AUTH0_ALGORITHMS = ["RS256"]