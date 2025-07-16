from lib.models.listing import Listing

class ListingRepo:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute(
            """
            SELECT * from listings
            """
            )
        listings = []
        for row in rows:
            listing = Listing(
                id=row['id'],
                host_id=row['host_id'],
                title=row['title'],
                description=row['description'],
                address=row['address'],
                city=row['city'],
                state=row['state'],
                country=row['country'],
                price_per_night=row['price_per_night'],
                max_guests=row['max_guest'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            listings.append(listing)
        return listings

    def find(self, listing_id):
        rows = self._connection.execute(
            """
            SELECT * from listings WHERE id = %s
            """
            , [listing_id])
        row = rows[0]
        return Listing(
                id=row['id'],
                host_id=row['host_id'],
                title=row['title'],
                description=row['description'],
                address=row['address'],
                city=row['city'],
                state=row['state'],
                country=row['country'],
                price_per_night=row['price_per_night'],
                max_guests=row['max_guest'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )

    def create(self, listing):
        rows = self._connection.execute(
            """
            INSERT INTO listings (host_id, title, description, address, city, state, country, price_per_night, max_guests) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """
            , [listing.host_id,  listing.title, listing.description, listing.address, listing.city, listing.state, listing.country, listing.price_per_night, listing.max_guests])
        new_id = rows[0]['id']
        return self.find(new_id)

    def delete(self, listing_id):
        self._connection.execute(
            """
            DELETE FROM listings WHERE id = %s
            """
            , [listing_id])
        return None