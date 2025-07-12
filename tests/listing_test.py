import pytest
from lib.models.listing import Listing

@pytest.fixture
def listing():
    return Listing(1, 1, 'Cozy Apartment in Central London', 'A charming one-bedroom apartment right in the heart of London, perfect for a couple or solo traveler.', '10 Downing St', 'London', 'England', 'United Kingdom', 120.00, 2)

def test_listing_constructs(listing):
    assert isinstance(listing, Listing)

def test_listing_formats_nicely(listing):
    assert str(listing) == "listing(1, 1, Cozy Apartment in Central London, A charming one-bedroom apartment right in the heart of London, perfect for a couple or solo traveler., 10 Downing St, London, England, United Kingdom, 120.00, 2)"

def test_artists_are_equal():
    listing_1 = Listing(1, 1, 'Cozy Apartment in Central London', 'A charming one-bedroom apartment right in the heart of London, perfect for a couple or solo traveler.', '10 Downing St', 'London', 'England', 'United Kingdom', 120.00, 2)
    listing_2 = Listing(1, 1, 'Cozy Apartment in Central London', 'A charming one-bedroom apartment right in the heart of London, perfect for a couple or solo traveler.', '10 Downing St', 'London', 'England', 'United Kingdom', 120.00, 2)
    assert listing_1 == listing_2
