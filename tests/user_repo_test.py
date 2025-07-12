from lib.repos.user_repo import UserRepo
from lib.models.user import User
from datetime import datetime

def test_get_all_records(db_connection):
    db_connection.seed("seeds/bnb_seed.sql")
    repository = UserRepo(db_connection)

    users = repository.all()

    # Assert on the results
    assert users == [
        User(1, 'johndoe', 'john.doe@example.com', 'hashedpassword123', 'John', 'Doe'),
        User(2, 'janesmith', 'jane.smith@example.com', 'anotherhash456', 'Jane', 'Smith'),
        User(3, 'petermiller', 'peter.miller@example.com', 'millerspass789', 'Peter', 'Miller'),
        User(4, 'alicejones', 'alice.jones@example.com', 'joneshash101', 'Alice', 'Jones'),
        User(5, 'emilywhite', 'emily.white@example.com', 'whitepass202', 'Emily', 'White')
    ]

# """
# When we call ArtistRepository#find
# We get a single Artist object reflecting the seed data.
# """
# def test_get_single_record(db_connection):
#     db_connection.seed("seeds/music_library.sql")
#     repository = ArtistRepository(db_connection)

#     artist = repository.find(3)
#     assert artist == Artist(3, "Taylor Swift", "Pop")

# """
# When we call ArtistRepository#create
# We get a new record in the database.
# """
# def test_create_record(db_connection):
#     db_connection.seed("seeds/music_library.sql")
#     repository = ArtistRepository(db_connection)

#     repository.create(Artist(None, "The Beatles", "Rock"))

#     result = repository.all()
#     assert result == [
#         Artist(1, "Pixies", "Rock"),
#         Artist(2, "ABBA", "Pop"),
#         Artist(3, "Taylor Swift", "Pop"),
#         Artist(4, "Nina Simone", "Jazz"),
#         Artist(5, "The Beatles", "Rock"),
#     ]

# """
# When we call ArtistRepository#delete
# We remove a record from the database.
# """
# def test_delete_record(db_connection):
#     db_connection.seed("seeds/music_library.sql")
#     repository = ArtistRepository(db_connection)
#     repository.delete(3) # Apologies to Taylor Swift fans

#     result = repository.all()
#     assert result == [
#         Artist(1, "Pixies", "Rock"),
#         Artist(2, "ABBA", "Pop"),
#         Artist(4, "Nina Simone", "Jazz"),
#     ]