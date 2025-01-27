from config import Logging

logger = Logging.setup_logging()


def search_created_booking_in_bookings(booking_ids, current_booking_id):
    logger.info(f"Booking ID we are trying to find: {current_booking_id}")

    matching_bookings = [booking['bookingid'] for booking in booking_ids if booking['bookingid'] == current_booking_id]

    if matching_bookings:
        logger.info(f"Booking ID {current_booking_id} was found in the list.")
    else:
        logger.warning(f"Booking ID {current_booking_id} was not found in the list.")

    return matching_bookings

