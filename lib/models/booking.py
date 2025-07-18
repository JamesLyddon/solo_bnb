from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Booking:
    id: int = None
    listing_id: int = None
    guest_id: int = None
    start_date: datetime = None
    end_date: datetime = None
    total_price: Decimal = None
    status: str = None
    created_at: datetime = None
    updated_at: datetime = None
        
    def __str__(self):
        return f"Booking({self.id}, {self.listing_id}, {self.guest_id}, {self.start_date}, {self.end_date}, {self.total_price:.2f}, {self.status})"

    # These next two methods will be used by the controller to check if
    # books are valid and if not show errors to the user.
    def is_valid(self):
        if self.listing_id == None or self.username == "":
            return False
        if self.guest_id == None or self.email == "":
            return False
        if self.start_date == None or self.password_hash == "":
            return False
        if self.end_date == None or self.first_name == "":
            return False
        if self.total_price == None or self.last_name == "":
            return False
        if self.status == None or self.last_name == "":
            return False
        return True

    def generate_errors(self):
        errors = []
        if self.listing_id == None or self.listing_id == "":
            errors.append("listing_id can't be blank")
        if self.guest_id == None or self.guest_id == "":
            errors.append("guest_id can't be blank")
        if self.start_date == None or self.start_date == "":
            errors.append("start_date can't be blank")
        if self.end_date == None or self.end_date == "":
            errors.append("end_date name can't be blank")
        if self.total_price == None or self.total_price == "":
            errors.append("total_price name can't be blank")
        if self.status == None or self.status == "":
            errors.append("status name can't be blank")
        if len(errors) == 0:
            return None
        else:
            return ", ".join(errors)