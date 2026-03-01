import json
from typing import TYPE_CHECKING, Any, Optional

from config import Logging

logger = Logging.setup_logging()


class Response:
    """Wrapper for a request response. Always sets status_code, result, and response_valid."""

    def __init__(self, response) -> None:
        self.status_code = response.status_code
        self.result: Optional[dict] = None
        self.response_valid = False

        try:
            if response.content:
                self.result = response.json()
            self.response_valid = response.ok and self.result is not None
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            logger.error(f"Error processing response: {e}")
            self.response_valid = False

    def get(self, key: str, default: Any = None) -> Any:
        """Return result[key] if result is a dict, else default."""
        if self.result is None:
            return default
        return self.result.get(key, default)

    @property
    def booking(self) -> Optional["Booking"]:
        """Parse result as a Booking model for typed, Pythonic access (e.g. response.booking.first_name). None if result is not a booking dict."""
        from models.booking import Booking

        if not self.result or not isinstance(self.result, dict) or "firstname" not in self.result:
            return None
        try:
            return Booking.model_validate(self.result)
        except Exception as e:
            logger.warning(f"Could not parse result as Booking: {e}")
            return None


if TYPE_CHECKING:
    from models.booking import Booking
