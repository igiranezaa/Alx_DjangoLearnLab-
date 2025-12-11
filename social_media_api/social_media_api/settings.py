from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "replace-this-in-production"

# Production requirement for ALX
DEBUG = False

ALLOWED_HOSTS = ["*"]


# -----------------------------
# APPLICATIONS
# -----------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "rest_framework.authtoken",

    # Local apps
    "accounts",
    "posts",
    "notifications",
]


# -----------------------------
# MIDDLEWARE
# -----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "social_media_api.urls"


# -----------------------------
# TEMPLATES
# -----------------------------
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
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "social_media_api.wsgi.application"


# -----------------------------
# DATABASE (DEFAULT SQLite)
# -----------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# -----------------------------
# PASSWORD VALIDATION
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# -----------------------------
# INTERNATIONALIZATION
# -----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# -----------------------------
# STATIC FILES
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# -----------------------------
# CUSTOM USER MODEL
# -----------------------------
AUTH_USER_MODEL = "accounts.User"


# -----------------------------
# REST FRAMEWORK
# -----------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}


# -----------------------------
# SECURITY HEADERS (ALX REQUIRED)
# -----------------------------
SECURE_BROWSER_XSS_FILTER = True           # ALX REQUIRED STRING
X_FRAME_OPTIONS = "DENY"                   # ALX REQUIRED STRING
SECURE_CONTENT_TYPE_NOSNIFF = True         # ALX REQUIRED STRING
SECURE_SSL_REDIRECT = True                 # ALX REQUIRED STRING

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# -----------------------------
# DEFAULT AUTO FIELD
# -----------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
