import os
import logging

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class UserData:
    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')


class Urls:
    BASE_URL = "https://restful-booker.herokuapp.com/booking"
    AUTH_URL = "https://restful-booker.herokuapp.com/auth"


class Statuses:
    STATUS_CREATED = 201


class Logging:
    def setup_logging(level=logging.INFO):
        logging.basicConfig(level=level)
        logger = logging.getLogger(__name__)
        return logger
