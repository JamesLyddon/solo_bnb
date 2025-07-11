-- First, we must delete (drop) all our tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS listings;
DROP TABLE IF EXISTS listing_images;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS listing_amenities;

-- Then, we recreate them
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE listings (
    id SERIAL PRIMARY KEY,
    host_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) NOT NULL,
    price_per_night NUMERIC(10, 2) NOT NULL,
    max_guests INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users(id)
);

CREATE TABLE listing_images (
    id SERIAL PRIMARY KEY,
    listing_id INT NOT NULL,
    image_url VARCHAR(2048) NOT NULL, -- VARCHAR(2048) is a common choice for URL length
    FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    listing_id INT NOT NULL,
    guest_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_price NUMERIC(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- e.g., 'pending', 'confirmed', 'canceled'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE,
    FOREIGN KEY (guest_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (end_date >= start_date), -- Ensures end date is not before start date
    CHECK (total_price >= 0) -- Ensures price is not negative
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    booking_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (rating >= 1 AND rating <= 5) -- Ensures rating is within a valid range
);

CREATE TABLE amenities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE listing_amenities (
    listing_id INT NOT NULL,
    amenity_id INT NOT NULL,
    PRIMARY KEY (listing_id, amenity_id), -- Composite Primary Key
    FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- Finally, we add any records that are needed for the tests to run
-- Insert Test Data

-- 1. Users
INSERT INTO users (username, email, password_hash, first_name, last_name) VALUES
('johndoe', 'john.doe@example.com', 'hashedpassword123', 'John', 'Doe'),
('janesmith', 'jane.smith@example.com', 'anotherhash456', 'Jane', 'Smith'),
('petermiller', 'peter.miller@example.com', 'millerspass789', 'Peter', 'Miller'),
('alicejones', 'alice.jones@example.com', 'joneshash101', 'Alice', 'Jones'),
('emilywhite', 'emily.white@example.com', 'whitepass202', 'Emily', 'White');

-- 2. Listings
-- John Doe (id=1) hosts a few
INSERT INTO listings (host_id, title, description, address, city, state, country, price_per_night, max_guests) VALUES
(1, 'Cozy Apartment in Central London', 'A charming one-bedroom apartment right in the heart of London, perfect for a couple or solo traveler.', '10 Downing St', 'London', 'England', 'United Kingdom', 120.00, 2),
(1, 'Spacious Family Home in Countryside', 'Beautiful detached house with a large garden, ideal for family holidays. Close to scenic walking trails.', 'Rural Lane 5', 'Oxford', 'England', 'United Kingdom', 250.00, 6);

-- Jane Smith (id=2) hosts one
INSERT INTO listings (host_id, title, description, address, city, state, country, price_per_night, max_guests) VALUES
(2, 'Beachfront Villa with Ocean Views', 'Luxury villa directly on the coast, stunning views and private beach access. Perfect for a relaxing getaway.', 'Ocean Drive 123', 'Brighton', 'England', 'United Kingdom', 350.50, 4);

-- Peter Miller (id=3) hosts one
INSERT INTO listings (host_id, title, description, address, city, state, country, price_per_night, max_guests) VALUES
(3, 'Charming Edinburgh Loft', 'Stylish loft apartment in the historic Old Town of Edinburgh. Ideal for exploring the city on foot.', 'Royal Mile 42', 'Edinburgh', 'Scotland', 'United Kingdom', 150.00, 3);

-- Alice Jones (id=4) hosts one
INSERT INTO listings (host_id, title, description, address, city, state, country, price_per_night, max_guests) VALUES
(4, 'Rustic Cottage in Scottish Highlands', 'Escape to the tranquil beauty of the Highlands in this quaint stone cottage. Perfect for nature lovers.', 'Loch Ness Road', 'Inverness', 'Scotland', 'United Kingdom', 90.00, 4);

-- 3. Listing Images
-- Images for London Apartment (listing_id=1)
INSERT INTO listing_images (listing_id, image_url) VALUES
(1, 'https://example.com/images/london_apt_1.jpg'),
(1, 'https://example.com/images/london_apt_2.jpg'),
(1, 'https://example.com/images/london_apt_3.jpg');

-- Images for Countryside Home (listing_id=2)
INSERT INTO listing_images (listing_id, image_url) VALUES
(2, 'https://example.com/images/country_house_1.jpg'),
(2, 'https://example.com/images/country_house_2.jpg');

-- Images for Beachfront Villa (listing_id=3)
INSERT INTO listing_images (listing_id, image_url) VALUES
(3, 'https://example.com/images/beach_villa_1.jpg'),
(3, 'https://example.com/images/beach_villa_2.jpg'),
(3, 'https://example.com/images/beach_villa_3.jpg');

-- Images for Edinburgh Loft (listing_id=4)
INSERT INTO listing_images (listing_id, image_url) VALUES
(4, 'https://example.com/images/edinburgh_loft_1.jpg');

-- 4. Amenities
INSERT INTO amenities (name) VALUES
('Wi-Fi'),
('Pool'),
('Kitchen'),
('Free Parking'),
('Air Conditioning'),
('Heating'),
('TV'),
('Washer'),
('Dryer'),
('Pet Friendly'),
('Hot Tub'),
('Fireplace');

-- 5. Listing Amenities (linking listings to amenities)
-- London Apartment (listing_id=1)
INSERT INTO listing_amenities (listing_id, amenity_id) VALUES
(1, (SELECT id FROM amenities WHERE name = 'Wi-Fi')),
(1, (SELECT id FROM amenities WHERE name = 'Kitchen')),
(1, (SELECT id FROM amenities WHERE name = 'Heating')),
(1, (SELECT id FROM amenities WHERE name = 'TV'));

-- Countryside Home (listing_id=2)
INSERT INTO listing_amenities (listing_id, amenity_id) VALUES
(2, (SELECT id FROM amenities WHERE name = 'Wi-Fi')),
(2, (SELECT id FROM amenities WHERE name = 'Kitchen')),
(2, (SELECT id FROM amenities WHERE name = 'Free Parking')),
(2, (SELECT id FROM amenities WHERE name = 'Washer')),
(2, (SELECT id FROM amenities WHERE name = 'Dryer')),
(2, (SELECT id FROM amenities WHERE name = 'Pet Friendly')),
(2, (SELECT id FROM amenities WHERE name = 'Fireplace'));

-- Beachfront Villa (listing_id=3)
INSERT INTO listing_amenities (listing_id, amenity_id) VALUES
(3, (SELECT id FROM amenities WHERE name = 'Wi-Fi')),
(3, (SELECT id FROM amenities WHERE name = 'Pool')),
(3, (SELECT id FROM amenities WHERE name = 'Kitchen')),
(3, (SELECT id FROM amenities WHERE name = 'Air Conditioning')),
(3, (SELECT id FROM amenities WHERE name = 'Hot Tub'));

-- Edinburgh Loft (listing_id=4)
INSERT INTO listing_amenities (listing_id, amenity_id) VALUES
(4, (SELECT id FROM amenities WHERE name = 'Wi-Fi')),
(4, (SELECT id FROM amenities WHERE name = 'Kitchen')),
(4, (SELECT id FROM amenities WHERE name = 'Heating')),
(4, (SELECT id FROM amenities WHERE name = 'TV'));

-- Rustic Cottage (listing_id=5)
INSERT INTO listing_amenities (listing_id, amenity_id) VALUES
(5, (SELECT id FROM amenities WHERE name = 'Kitchen')),
(5, (SELECT id FROM amenities WHERE name = 'Free Parking')),
(5, (SELECT id FROM amenities WHERE name = 'Fireplace')),
(5, (SELECT id FROM amenities WHERE name = 'Pet Friendly'));


-- 6. Bookings
-- Alice Jones (user_id=4) books London Apartment (listing_id=1)
INSERT INTO bookings (listing_id, guest_id, start_date, end_date, total_price, status) VALUES
(1, 4, '2025-08-10', '2025-08-15', 600.00, 'confirmed'); -- 5 nights * 120

-- Emily White (user_id=5) books Beachfront Villa (listing_id=3)
INSERT INTO bookings (listing_id, guest_id, start_date, end_date, total_price, status) VALUES
(3, 5, '2025-09-01', '2025-09-07', 2103.00, 'pending'); -- 6 nights * 350.50

-- John Doe (user_id=1) books Edinburgh Loft (listing_id=4) - testing a host booking their own type of listing (though not their own specific listing)
INSERT INTO bookings (listing_id, guest_id, start_date, end_date, total_price, status) VALUES
(4, 1, '2025-07-20', '2025-07-23', 450.00, 'confirmed'); -- 3 nights * 150

-- Jane Smith (user_id=2) books Rustic Cottage (listing_id=5)
INSERT INTO bookings (listing_id, guest_id, start_date, end_date, total_price, status) VALUES
(5, 2, '2026-01-05', '2026-01-12', 630.00, 'confirmed'); -- 7 nights * 90


-- 7. Reviews
-- Alice Jones reviews London Apartment (booking_id=1)
INSERT INTO reviews (booking_id, reviewer_id, rating, comment) VALUES
(1, 4, 5, 'Absolutely fantastic stay! The apartment was clean, comfortable, and perfectly located. John was a great host.'),
(1, 4, 4, 'Great location, but the wifi was a bit spotty sometimes. Still, a lovely place.'); -- Example of multiple reviews on same booking, if your logic supports it. Typically one per booking. If not, remove the second one.

-- John Doe reviews Edinburgh Loft (booking_id=3)
INSERT INTO reviews (booking_id, reviewer_id, rating, comment) VALUES
(3, 1, 4, 'Charming place in a vibrant area. The host was very responsive. A little noisy at night, but expected for the location.');

-- Jane Smith reviews Rustic Cottage (booking_id=4)
INSERT INTO reviews (booking_id, reviewer_id, rating, comment) VALUES
(4, 2, 5, 'A truly magical escape! The cottage was cozy and the surrounding nature was breathtaking. Highly recommend for a peaceful retreat.');