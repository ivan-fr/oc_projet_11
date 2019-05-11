import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STOP_WORDS_FILE = os.path.join(BASE_DIR, "grandpyapp", "static",
                               "stop_words.json")
COUNTRIES_FILE = os.path.join(BASE_DIR, "grandpyapp", "static",
                              "countries.json")

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
GOOGLE_API_KEY = "AIzaSyABktea4rFaWShQm7F25YWXgAuv9f-nFvk"

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,
                                                          'grandpyapp.db')
    SQLALCHEMY_DATABASE_URI_TEST = os.environ.get('DATABASE_URL') or \
                                   'sqlite:///' + os.path.join(BASE_DIR,
                                                               'test.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = os.path.join(BASE_DIR, "grandpyapp", "static", "uploads")

MAX_CONTENT_LENGTH = 16 * 1024 * 1024
