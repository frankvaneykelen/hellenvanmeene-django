from .base import *  # noqa: F401, F403

DEBUG = False

# Azure App Service sets WEBSITE_HOSTNAME
import os
ALLOWED_HOSTS = [
    os.environ.get("WEBSITE_HOSTNAME", ""),
    "hellenvanmeene.com",
    "www.hellenvanmeene.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://hellenvanmeene.com",
    "https://www.hellenvanmeene.com",
    f"https://{os.environ.get('WEBSITE_HOSTNAME', '')}",
]

# Security headers
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging – send errors to admins via email
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
