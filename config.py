"""App configuration. Credentials are read from env; call reload_credentials() to re-read after .env may have been loaded."""
import os
import logging

from dotenv import load_dotenv

load_dotenv()


class UserData:
    """Credentials from env. Set LOGIN and PASSWORD in .env. Use reload_credentials() to re-read after late .env load."""
    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')


def reload_credentials() -> None:
    """Re-load .env and refresh UserData.LOGIN and UserData.PASSWORD. Call before using credentials if .env might have been loaded after config was imported."""
    load_dotenv()
    UserData.LOGIN = os.getenv('LOGIN')
    UserData.PASSWORD = os.getenv('PASSWORD')


class Urls:
    BASE_URL = "https://restful-booker.herokuapp.com/booking"
    AUTH_URL = "https://restful-booker.herokuapp.com/auth"


class Statuses:
    STATUS_OK = 200
    STATUS_CREATED = 201


class Logging:
    @staticmethod
    def setup_logging(level=logging.INFO):
        logging.basicConfig(level=level)
        logger = logging.getLogger(__name__)
        return logger
