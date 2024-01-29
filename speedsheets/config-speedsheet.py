"""
Database
"""
DB_NAME = 
DB_USER = 
DB_PASSWORD = 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


"""
Staticfiles
"""
STATICFILES_DIRS = [
    Path.joinpath(BASE_DIR, 'static'),
    Path.joinpath(BASE_DIR, 'media'),
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = Path.joinpath(BASE_DIR, 'static_cdn')
MEDIA_ROOT = Path.joinpath(BASE_DIR, 'media_cdn')

BASE_URL = "http://127.0.0.1:8000"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""
Authentication and backend
"""
AUTH_USER_MODEL = 'account.BaseAccount'
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # During development only
AUTHENTICATION_BACKENDS = ( 
    'django.contrib.auth.backends.AllowAllUsersModelBackend', 
    'account.backends.CaseInsensitiveModelBackend',
    )