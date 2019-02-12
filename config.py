import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STOP_WORDS_FILE = os.path.join(BASE_DIR, "grandpyapp", "static",
                               "stop_words.json")
COUNTRIES_FILE = os.path.join(BASE_DIR, "grandpyapp", "static",
                              "countries.json")

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
GOOGLE_API_KEY = "AIzaSyCIB8gP3P5S-ttaOCZQBj0efd8sSDbPqdQ"

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                          'sqlite:///' + os.path.join(BASE_DIR, 'grandpyapp.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = os.path.join(BASE_DIR, "grandpyapp", "static", "uploads")

MAX_CONTENT_LENGTH = 16 * 1024 * 1024
