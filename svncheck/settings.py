"""
Django settings for svncheck project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e-gme+c%nr4l6pw&6wc_)hh7nm%e9))dlixi%@(s3mf$nlxvkd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_user',
    'app_svn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'svncheck.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'svncheck.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        # sqlite
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        # mysql
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'svncheck',
        'USER': 'mysql',
        'PASSWORD': 'mysql',
        'HOST': '10.16.34.145',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


# 修改settings里这个变量自己写，引号里的路径是工程里的static目录名
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# session 设置
SESSION_COOKIE_AGE = 60 * 30  # 30分钟
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 关闭浏览器，则COOKIE失效


# log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }, # 针对 DEBUG = True 的情况
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s==========%(levelname)s==========%(pathname)s %(lineno)d: %(message)s'
        },
        # INFO 2016-09-03 16:25:20,067 /home/ubuntu/mysite/views.py  get 29: some info...
    },
    'handlers': { # 定义输出形式
        'mail_admins': { # mail
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
             'formatter':'standard'
        },
        'file_handler': { # 用于文件输出
             'level': 'ERROR',
             'class': 'logging.handlers.TimedRotatingFileHandler',
             'filename': 'D:\workspace\log\django.log',
             # 'filename': '/home/yant/log/django.log',
             'formatter':'standard'
        },
        'console':{
            'level': 'INFO',
            'filters': ['require_debug_true'], # 上面的filter
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers' : [
                'file_handler',
                # 'console'
            ],
            'level': 'INFO',
            'propagate': True # 是否继承父类的log信息
        }, # handlers 来自于上面的 handlers 定义的内容
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
