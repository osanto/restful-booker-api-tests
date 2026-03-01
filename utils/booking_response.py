import json
from typing import TYPE_CHECKING, Any, Optional

from config import Logging

logger = Logging.setup_logging()

# response.json() can return a dict (e.g. single booking) or a list (e.g. get_all_booking_ids)
JsonBody = dict[str, Any] | list[Any]


class Response:
    """Wrapper for a request response. Always sets status_code, result, and response_valid. result is dict or list depending on endpoint."""

    def __init__(self, response) -> None:
        self.status_code = response.status_code
        self.result: Optional[JsonBody] = None
        self.response_valid = False
        self.error_message: Optional[str] = None

        try:
            if response.content:
                self.result = response.json()
            self.response_valid = response.ok and self.result is not None
            
            if not response.ok:
                if isinstance(self.result, dict):
                    self.error_message = self.result.get("error") or self.result.get("message") or response.reason
                else:
                    self.error_message = response.reason
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            logger.error(f"Error processing response: {e}")
            self.response_valid = False
            self.error_message = f"Failed to parse response: {str(e)}"

    def get(self, key: str, default: Any = None) -> Any:
        """Return result[key] if result is a dict, else default. No-op when result is a list."""
        if self.result is None or not isinstance(self.result, dict):
            return default
        return self.result.get(key, default)

    @property
    def is_client_error(self) -> bool:
        """True if status code is 4xx (client error)."""
        return 400 <= self.status_code < 500

    @property
    def is_server_error(self) -> bool:
        """True if status code is 5xx (server error)."""
        return 500 <= self.status_code < 600

    @property
    def booking_id(self) -> Optional[int]:
        """Booking ID from create response (result['bookingid']). None if missing or result is not a dict."""
        value = self.get("bookingid")
        return int(value) if value is not None else None

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
