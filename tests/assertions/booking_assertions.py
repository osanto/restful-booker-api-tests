from config import Logging

logger = Logging.setup_logging()


def assert_that_booking_amount_greater_than_zero(response):
    bookings_amount = len(response)
    logger.info(f"Total amount of records is: {bookings_amount}")
    assert bookings_amount > 0, f"Expected amount of bookings to be greater than 0, but got {bookings_amount}"
