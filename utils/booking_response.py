import json
from dataclasses import dataclass
from config import Logging

logger = Logging.setup_logging()


@dataclass
class Response:
    status_code: int
    result: dict = None
    response_valid: bool = False

    def __init__(self, response):
        self.status_code = response.status_code

        if response.ok:
            try:
                self.result = response.json()
                self.response_valid = True
            except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
                logger.error(f"Error processing response: {e}")
                self.response_valid = False

