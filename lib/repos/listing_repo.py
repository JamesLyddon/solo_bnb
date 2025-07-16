from lib.models.listing import Listing
from lib.models.user import User
from decimal import Decimal
from datetime import datetime, date
from collections import defaultdict # Useful for grouping results
from typing import Optional
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
                max_guests=row['max_guests'],
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
                max_guests=row['max_guests'],
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
    
# -------------

    def all_with_details(self) -> list[Listing]:
        """
        Fetches all listings, including their associated image URLs and host usernames.
        """
        sql = """
            SELECT
                l.id AS listing_id,
                l.host_id,
                l.title,
                l.description,
                l.address,
                l.city,
                l.state,
                l.country,
                l.price_per_night,
                l.max_guests,
                l.created_at AS listing_created_at,
                l.updated_at AS listing_updated_at,
                u.username AS host_username,
                li.image_url AS image_url, -- Alias image_url from listing_images
                li.id AS image_id -- Include image ID to differentiate multiple images
            FROM
                listings AS l
            JOIN
                users AS u ON l.host_id = u.id
            LEFT JOIN
                listing_images AS li ON l.id = li.listing_id
            ORDER BY
                l.id, li.id; -- Order by listing ID then image ID to group results
        """

        rows = self._connection.execute(sql)

        # Use a dictionary to group results by listing_id
        listings_map = defaultdict(lambda: {
            'listing': None,
            'image_urls': []
        })

        for row in rows:
            listing_id = row['listing_id']

            # If this is the first time we see this listing_id, create the base Listing object
            if listings_map[listing_id]['listing'] is None:
                listings_map[listing_id]['listing'] = Listing(
                    id=row['listing_id'],
                    host_id=row['host_id'],
                    title=row['title'],
                    description=row['description'],
                    address=row['address'],
                    city=row['city'],
                    state=row['state'],
                    country=row['country'],
                    price_per_night=Decimal(str(row['price_per_night'])),
                    max_guests=row['max_guests'],
                    created_at=row['listing_created_at'],
                    updated_at=row['listing_updated_at'],
                    host_username=row['host_username']
                )

            # Add the image URL if it exists (LEFT JOIN means image_url can be NULL)
            if row['image_url']:
                listings_map[listing_id]['image_urls'].append(row['image_url'])

        # Now, construct the final list of Listing objects
        final_listings = []
        for item in listings_map.values():
            listing = item['listing']
            listing.image_urls = item['image_urls'] # Assign the collected image URLs
            final_listings.append(listing)

        return final_listings


    def find_by_id_with_details(self, listing_id: int) -> Optional[Listing]:
        """
        Fetches a single listing by ID, including its associated image URLs and host username.
        """
        sql = """
            SELECT
                l.id AS listing_id,
                l.host_id,
                l.title,
                l.description,
                l.address,
                l.city,
                l.state,
                l.country,
                l.price_per_night,
                l.max_guests,
                l.created_at AS listing_created_at,
                l.updated_at AS listing_updated_at,
                u.username AS host_username,
                li.image_url AS image_url
            FROM
                listings AS l
            JOIN
                users AS u ON l.host_id = u.id
            LEFT JOIN
                listing_images AS li ON l.id = li.listing_id
            WHERE l.id = %s
            ORDER BY li.id; -- Order by image ID to ensure consistent order
        """

        rows = self._connection.execute(sql, [listing_id])

        if not rows:
            return None # Listing not found

        # For a single listing, create the base object from the first row
        # and then collect all image URLs from all subsequent rows.
        listing = Listing(
            id=rows[0]['listing_id'],
            host_id=rows[0]['host_id'],
            title=rows[0]['title'],
            description=rows[0]['description'],
            address=rows[0]['address'],
            city=rows[0]['city'],
            state=rows[0]['state'],
            country=rows[0]['country'],
            price_per_night=Decimal(str(rows[0]['price_per_night'])),
            max_guests=rows[0]['max_guests'],
            created_at=rows[0]['listing_created_at'],
            updated_at=rows[0]['listing_updated_at'],
            host_username=rows[0]['host_username']
        )

        # Collect all image URLs
        for row in rows:
            if row['image_url']: # Only add if image_url is not NULL (from LEFT JOIN)
                listing.image_urls.append(row['image_url'])

        return listing