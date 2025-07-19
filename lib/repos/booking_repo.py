from lib.models.booking import Booking
from lib.models.listing import Listing
from lib.models.user import User
from decimal import Decimal
from datetime import datetime, date
from collections import defaultdict # Useful for grouping results
from typing import Optional

class BookingRepo:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute(
            """
            SELECT * from bookings
            """
            )
        bookings = []
        for row in rows:
            booking = Booking(
                id=row['id'],
                listing_id=row['listing_id'],
                guest_id=row['guest_id'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                total_price=row['total_price'],
                status=row['status'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            bookings.append(booking)
        return bookings

    def find(self, booking_id):
        rows = self._connection.execute(
            """
            SELECT * from bookings WHERE id = %s
            """
            , [booking_id])
        row = rows[0]
        return Booking(
                id=row['id'],
                listing_id=row['listing_id'],
                guest_id=row['guest_id'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                total_price=row['total_price'],
                status=row['status'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )

    def create(self, booking):
        rows = self._connection.execute(
            """
            INSERT INTO bookings (listing_id, guest_id, start_date, end_date, total_price, status) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """
            , [booking.listing_id,  booking.guest_id, booking.start_date, booking.end_date, booking.total_price, booking.status])
        new_id = rows[0]['id']
        
        return self.find(new_id)

    def delete(self, booking_id):
        self._connection.execute(
            """
            DELETE FROM bookings WHERE id = %s
            """
            , [booking_id])
        return None
