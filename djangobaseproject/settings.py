import os
from pathlib import Path

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
BASE_DIR = Path(__file__).resolve().parent.parent

SHARED_URL = "https://shared.acdh.oeaw.ac.at/"
PROJECT_NAME = "djangobaseproject"
ACDH_IMPRINT_URL = "https://shared.acdh.oeaw.ac.at/acdh-common-assets/api/imprint.php?serviceID="
REDMINE_ID = 17013
SECRET_KEY = os.environ.get("SECRET_KEY", "vxAeLYeo")
if os.environ.get("DEBUG"):
    DEBUG = True
else:
    DEBUG = False
ADD_ALLOWED_HOST = os.environ.get("ALLOWED_HOST", "*")
ALLOWED_HOSTS = [
    "127.0.0.1",
    "0.0.0.0",
    ADD_ALLOWED_HOST,
]

# Application definition

INSTALLED_APPS = [
    'dal',
    'django.contrib.admin',
    'dal_select2',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reversion',
    'django_extensions',
    "crispy_forms",
    "crispy_bootstrap4",
    'django_filters',
    'django_tables2',
    'rest_framework',
    'django_spaghetti',
    'leaflet',
    'netvis',
    'charts',
    'idprovider',
    'webpage',
    'browsing',
    'vocabs',
    'infos',
    'aschach',
    'tei',
    'archeutils'
]

CRISPY_TEMPLATE_PACK = "bootstrap4"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SPAGHETTI_SAUCE = {
    "apps": [
        "aschach", "vocabs",
    ],
    "show_fields": False,
    "exclude": {"auth": ["user"]},
}


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reversion.middleware.RevisionMiddleware',
]

ROOT_URLCONF = 'djangobaseproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'webpage.webpage_content_processors.installed_apps',
                'webpage.webpage_content_processors.is_dev_version',
                'webpage.webpage_content_processors.get_db_name',
                "webpage.webpage_content_processors.shared_url",
                "webpage.webpage_content_processors.my_app_name",
            ],
        },
    },
]

WSGI_APPLICATION = 'djangobaseproject.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": os.environ.get("POSTGRES_DB", "aschach"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'de'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")
STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = "/media/"

ARCHE_SETTINGS = {
    'project_name': ROOT_URLCONF.split('.')[0],
    'base_url': "https://id.acdh.oeaw.ac.at/donauhandel"
}

ARCHE_BASE_URL = "https://id.acdh.oeaw.ac.at/donauhandel"
ARCHE_LANG = 'de'

ARCHE_CONST_MAPPINGS = [
    ('hasOwner', "https://d-nb.info/gnd/13140007X",),  # Rauscher
    ('hasContact', "https://d-nb.info/gnd/13140007X",),
    ('hasRightsHolder', "https://d-nb.info/gnd/13140007X",),
    ('hasPrincipalInvestigator', "https://d-nb.info/gnd/13140007X",),
    ('hasLicensor', 'https://d-nb.info/gnd/13140007X',),
    ('hasCreator', 'https://d-nb.info/gnd/13140007X',),
    ('hasCreator', 'https://d-nb.info/gnd/1031446176',),  # Serles
    ('hasCreator', 'https://d-nb.info/gnd/103048337X',),  # Pamperl
    ('hasLicense', 'https://creativecommons.org/licenses/by/4.0/',),
    ('hasRelatedDiscipline', 'https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/601',),
    ('hasSubject', 'Handel',),
    ('hasSubject', 'Frühe Neuzeit',),
    ('hasMetadataCreator', 'https://d-nb.info/gnd/1043833846',),  # pandorfer
    ('hasDepositor', 'https://d-nb.info/gnd/1043833846',),  # pandorfer
]


PHAIDRA_BASE = "https://fedora.phaidra.univie.ac.at/fedora/objects/{}/methods/bdef:Content/get"

VOCABS_DEFAULT_PEFIX = 'donauhandel-norm'


VOCABS_SETTINGS = {
    'default_prefix': VOCABS_DEFAULT_PEFIX,
    'default_nsgg': "http://www.vocabs/{}/".format(VOCABS_DEFAULT_PEFIX),
    'default_lang': "de"
}

APPCREATOR_SPREADSHEET_ID = "1A08Iv--5cqbKM71U0ww32gDx5ZnXwEr3R1RAg3PjgYE"

LEAFLET_CONFIG = {
    'MAX_ZOOM': 18,
    'DEFAULT_CENTER': (48, 15),
    'DEFAULT_ZOOM': 8,
    'TILES': [
        (
            'BASIC',
            'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            {
                'attribution':
                    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>\
                    contributors',
                'maxZoom': 18,
            }
        )
    ],
}

DATA_REPO_URL = "https://raw.githubusercontent.com/donauhandel/aschach-data/main/orig_data/csvs/"
