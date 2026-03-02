from config import Logging
from models import BookingIdItem

logger = Logging.setup_logging()


def search_created_booking_in_bookings(booking_ids: list[BookingIdItem], current_booking_id: int) -> list[int]:
    """Search for a booking ID in a list of BookingIdItem objects. Returns list of matching IDs."""
    logger.info(f"Booking ID we are trying to find: {current_booking_id}")

    matching_bookings = [item.booking_id for item in booking_ids if item.booking_id == current_booking_id]

    if matching_bookings:
        logger.info(f"Booking ID {current_booking_id} was found in the list.")
    else:
        logger.warning(f"Booking ID {current_booking_id} was not found in the list.")

    return matching_bookings

