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