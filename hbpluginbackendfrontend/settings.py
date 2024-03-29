import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wzv$8xb5&94+^*oy9225ihsak%u6p8%z(+ybv#-=&8pk^q0h$j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'shopify',
    'corsheaders',
    'shiprocket',
    'hotellogix',
    'consolidate_hotelogix',
    'TallyExportXML',
    'consolidationsXML',
    'canaraSpring'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'hbpluginbackendfrontend.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'hbpluginbackendfrontend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


# Database Routings
DATABASE_ROUTERS = ['canaraSpring.routers.CanaraSprigRouter','consolidationsXML.routers.ConsolidationRouter','TallyExportXML.routers.TallyExportXMLRouter','consolidate_hotelogix.routers.hotelogixExcelRouter','hotellogix.routers.HotelRouter','shiprocket.routers.ShiprocketRouter','shopify.routers.ShopRouter']


DATABASES ={
        'default': {
        # 'NAME': 'testing',
        # 'ENGINE': 'django.db.backends.mysql',
        # 'USER': 'root',
        # 'PASSWORD':'root',
        },

        'canaraspring': {
        'NAME': 'canaraspringdb',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD':'root',
        },

        'consolidationxml': {
        'NAME': 'consolidationxmldb',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD':'root',
        },

        'tallyexport': {
        'NAME': 'tallyexportdb',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD':'root',
        },

        'hotel': {
        'NAME': 'hotelogixdb',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD':'root',
        },

        'hotelogixexcel': {
        'NAME': 'hotelogixExceldb',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD':'root',
        },

        'shiprocket': {
        'NAME': 'shiprocketdb',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD':'root',
        },

        'shopifytb': {
        'NAME': 'shopdb',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD':'root',
        },
    }


# 2nd Options
# DATABASE_ROUTERS = {
#     'myapp': 'myapp.routers.MyAppRouter',
#     'anotherapp': 'anotherapp.routers.AnotherAppRouter',
#     # Add more app-specific routers if needed
# }
    


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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = ["*"]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

STATIC_URL='/static/'
STATIC_ROOT=os.path.join(BASE_DIR, 'static/') 

MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR, 'media/')


