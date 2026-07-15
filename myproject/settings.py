"""
Django settings for myproject project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-q&t1z%y*2au4*d8@0!kmolk4oov$s)k296^%)2%1b8eed5z*-u'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django_select2",
   'django.contrib.humanize',
    'django_daisy',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp.apps.MyappConfig',
    "import_export",
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Aden'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Jazzmin Settings مع DaisyUI
JAZZMIN_SETTINGS = {
    "site_title": "🏫 نظام إدارة الطلاب",
    "site_header": "🏫 نظام إدارة الطلاب المتكامل",
    "site_brand": "🎓 الإدارة الأكاديمية",
    "site_logo": None,
    "login_logo": None,
    "welcome_sign": "مرحباً بك في النظام الأكاديمي المتكامل",
    "copyright": "النظام الأكاديمي © 2024",
    
    "theme": "lux",
    "dark_mode_theme": "darkly",
    
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "myapp.Student": "fas fa-user-graduate",
        "myapp.Course": "fas fa-book-open",
        "myapp.Enrollment": "fas fa-clipboard-list",
    },
    
    "order_with_respect_to": ["myapp", "myapp.Student", "myapp.Course", "myapp.Enrollment", "auth"],
    
    "language_chooser": False,
    "changeform_format": "horizontal_tabs",
    
    "topmenu_links": [
        {"name": "🏠 الرئيسية", "url": "/", "permissions": ["auth.view_user"]},
        {"name": "📊 لوحة التحكم", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app": "myapp"},
    ],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "lux",
    "dark_mode_theme": "darkly",
    "navbar": "navbar-dark",
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_flat_style": True,
    "accent": "accent-primary",
    "brand_colour": "navbar-primary",
}
