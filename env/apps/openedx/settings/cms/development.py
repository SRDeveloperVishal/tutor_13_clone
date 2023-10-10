# -*- coding: utf-8 -*-
import os
from cms.envs.devstack import *

LMS_BASE = "mohit.io:8000"
LMS_ROOT_URL = "http://" + LMS_BASE

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_KEY = "cms-sso-dev"
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = LMS_ROOT_URL

FEATURES["PREVIEW_LMS_BASE"] = "preview.mohit.io:8000"

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "host": "mongodb",
    "port": 27017,
    
    "user": None,
    "password": None,
    
    "db": "openedx",
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{
  
  "host": "elasticsearch",
  "port": 9200,
}]

CONTACT_MAILING_ADDRESS = "My Open edX - https://mohit.io"

DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]
# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)

import warnings
from django.utils.deprecation import RemovedInDjango40Warning, RemovedInDjango41Warning
warnings.filterwarnings("ignore", category=RemovedInDjango40Warning)
warnings.filterwarnings("ignore", category=RemovedInDjango41Warning)
warnings.filterwarnings("ignore", category=DeprecationWarning, module="lms.djangoapps.course_wiki.plugins.markdownedx.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "https://mohit.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "YpmIcnCkQwJzVjAHsiX2sGdD"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "QevjKKwaqKMV1vYEeTRcZ0LqpqF8OHk39wQM3nkDbYAhQTD11PwUVkQfZHnLily2kw7j5gKh55wKCI33ev8vtURGpY3ikDu9ao5DlmpMUjHGJmgfqTPWsnkUD6y34VwQXGm3uOyIkFk80dOwzZ7VXBScidfWwAQOKZaEHwTxNw4DpzHYhm8dFvs1mwoO7n9etS2MvNdCJO0TIrwU9cMWDKxtoTE2xnUgQ9J_bOnzsMZbDyNd0Mt5ACa7uBJFv0TnRuQ9KxUvTu6JAJXqjQBW4o5WKsKdWajlV5HPbqx3cBslALlBq4YaZ1z8RhRNYFVR2lJBwp2-lyuT9PPr4W-ggQ",
        "n": "teg2M9w_8t5U6sORLxztLQbw0YBHVao_VvFyemIFzfsdT7kxfw-v1HU_7PSjoEkibO0gJwwMyVQddFkT3X41H6ARAeGayXY4P2t9PLSvRV_UHC3auBlZ205Y3qiI6j9bC0wUSvsqXurSOPYiHmSI95eUie51UQXzr8TSCJds2IaZ_CET_QmDS2o81Sz2zSMq8HUEJ_YgqwNwGeMZyJn-rPb0_P3bSu88MvEc2Jj2TprwPs3BC18m0QKT8gy0plbqA8tN25WqFS0TCRgye69VD8Gxqmbw4Rlor2CzzUHWAhTq3tfbnlQ--VN48yIhUAv4GSNv-8CNo896ORkQudPKBw",
        "p": "ykGlPVN_9_31ByOAJjvwV7SQC2ZHvJKnQszmMj-KJSj0zbJsrvWZVRU8EWHmZH5jS7WOyZnCY62DwBHBY3E_F2vgbVBiU7X4R6v3siJ5pfJGXSR3MQny29UAfIeP088gz-Ks1tM6mnHmmlvTFggBbVR-nFG3VVrVJ6tloXTSoic",
        "q": "5j5Qz95WIjp2TYjODqtjXEsL_g47vElZF_BcsH_xQtQcxjLYJGHMDcfa_qokMdnwgOKDOusTw5htpbvL-gg-4TC5nd9b1yhSTs_OGEdUIAETrAlSzoS15j-kdRhWsCpCac1XbHp54L73CbeIF5WIyHiADFSbf6zJ_8P2pKdg5SE",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "teg2M9w_8t5U6sORLxztLQbw0YBHVao_VvFyemIFzfsdT7kxfw-v1HU_7PSjoEkibO0gJwwMyVQddFkT3X41H6ARAeGayXY4P2t9PLSvRV_UHC3auBlZ205Y3qiI6j9bC0wUSvsqXurSOPYiHmSI95eUie51UQXzr8TSCJds2IaZ_CET_QmDS2o81Sz2zSMq8HUEJ_YgqwNwGeMZyJn-rPb0_P3bSu88MvEc2Jj2TprwPs3BC18m0QKT8gy0plbqA8tN25WqFS0TCRgye69VD8Gxqmbw4Rlor2CzzUHWAhTq3tfbnlQ--VN48yIhUAv4GSNv-8CNo896ORkQudPKBw",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "https://mohit.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "YpmIcnCkQwJzVjAHsiX2sGdD"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}

FEATURES["ENABLE_DISCUSSION_SERVICE"] = True
######## End of settings common to LMS and CMS

######## Common CMS settings

STUDIO_NAME = u"My Open edX - Studio"

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "cxRzljq6yNOZWhOYVqQHpM2N"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "http://lms:8000"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False  # scheme is correctly included in redirect_uri

MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 100

FRONTEND_LOGIN_URL = LMS_ROOT_URL + '/login'
FRONTEND_LOGOUT_URL = LMS_ROOT_URL + '/logout'
FRONTEND_REGISTER_URL = LMS_ROOT_URL + '/register'

# Create folders if necessary
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE]:
    if not os.path.exists(folder):
        os.makedirs(folder)



######## End of common CMS settings

# Setup correct webpack configuration file for development
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"


