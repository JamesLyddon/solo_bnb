from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Listing:
    id: int = None
    host_id: int = None
    title: str = None
    description: str = None
    address: str = None
    city: str = None
    state: str = None
    country: str = None
    price_per_night: Decimal = None
    max_guests: int = None
    created_at: datetime = None
    updated_at: datetime = None

    def __str__(self):
        return f"listing({self.id}, {self.host_id}, {self.title}, {self.description}, {self.address}, {self.city}, {self.state}, {self.country}, {self.price_per_night:.2f}, {self.max_guests})"

    # These next two methods will be used by the controller to check if
    # listings are valid and if not show errors to the user.
    # state is ommitted as it's optional
    def is_valid(self):
        if self.host_id == None or self.host_id == "":
            return False
        if self.title == None or self.title == "":
            return False
        if self.description == None or self.description == "":
            return False
        if self.address == None or self.address == "":
            return False
        if self.city == None or self.city == "":
            return False
        if self.country == None or self.country == "":
            return False
        if self.price_per_night == None or self.price_per_night == "":
            return False
        if self.max_guests == None or self.max_guests == "":
            return False
        return True

    def generate_errors(self):
        errors = []

        if self.host_id == None or self.host_id == "":
            errors.append("Host ID can't be blank")
        if self.title == None or self.title == "":
            errors.append("Title can't be blank")
        if self.description == None or self.description == "":
            errors.append("Description can't be blank")
        if self.address == None or self.address == "":
            errors.append("Address can't be blank")
        if self.city == None or self.city == "":
            errors.append("City can't be blank")
        if self.country == None or self.country == "":
            errors.append("Country can't be blank")
        if self.price_per_night == None or self.price_per_night == "":
            errors.append("Price per night can't be blank")
        if self.max_guests == None or self.max_guests == "":
            errors.append("Max guests can't be blank")

        if len(errors) == 0:
            return None
        else:
            return ", ".join(errors)