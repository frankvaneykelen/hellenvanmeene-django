"""
Base settings shared by all environments.
Environment-specific values are loaded from a .env file via python-decouple.
"""

from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="")

# ---------------------------------------------------------------------------
# Apps
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "imagekit",
    "storages",
    # Third-party continued
    # Project apps
    "core",
    "photos",
    "exhibitions",
    "events",
    "news",
    "pages",
    "publications",
    "shop",
    "galleries",
    "links",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------------------------------
# Database – Azure SQL via mssql-django
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", default="1433"),
        "OPTIONS": {
            "driver": config("DB_DRIVER", default="ODBC Driver 18 for SQL Server"),
            "extra_params": "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30",
        },
    }
}

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URL = "/admin/"
LOGOUT_REDIRECT_URL = "/"

# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/Amsterdam"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------------------------------------------
# Media / Azure Blob Storage
# ---------------------------------------------------------------------------
AZURE_ACCOUNT_NAME = config("AZURE_STORAGE_ACCOUNT_NAME", default="")
AZURE_ACCOUNT_KEY = config("AZURE_STORAGE_ACCOUNT_KEY", default="")
AZURE_CONTAINER = config("AZURE_STORAGE_CONTAINER", default="media")
AZURE_CUSTOM_DOMAIN = config(
    "AZURE_STORAGE_CUSTOM_DOMAIN",
    default=f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net",
)

DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"
MEDIA_URL = f"https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/"

# ---------------------------------------------------------------------------
# Email – SendGrid via django-anymail
# ---------------------------------------------------------------------------
ANYMAIL = {
    "SENDGRID_API_KEY": config("SENDGRID_API_KEY", default=""),
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@hellenvanmeene.com")
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ---------------------------------------------------------------------------
# Migrations
# ---------------------------------------------------------------------------
# Legacy apps map to pre-existing tables; tell Django never to generate or
# apply migrations for them so their models are always taken from the current
# Python state rather than from a migration history that doesn't exist.
MIGRATION_MODULES = {
    "core": None,
    "photos": None,
    "exhibitions": None,
    "events": None,
    "news": None,
    "pages": None,
    "publications": None,
}

# ---------------------------------------------------------------------------
# Miscellaneous
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
