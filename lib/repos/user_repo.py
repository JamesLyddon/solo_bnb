from lib.models.user import User

class UserRepo:
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all users
    def all(self):
        rows = self._connection.execute('SELECT * from users')
        users = []
        for row in rows:
            item = User(row["id"], row["username"], row["email"], row["password_hash"], row["first_name"], row["last_name"])
            users.append(item)
        return users

    # # Find a single artist by their id
    # def find(self, artist_id):
    #     rows = self._connection.execute(
    #         'SELECT * from artists WHERE id = %s', [artist_id])
    #     row = rows[0]
    #     return Artist(row["id"], row["name"], row["genre"])

    # # Create a new artist
    # # Do you want to get its id back? Look into RETURNING id;
    # def create(self, artist):
    #     self._connection.execute('INSERT INTO artists (name, genre) VALUES (%s, %s)', [
    #                              artist.name, artist.genre])
    #     return None

    # # Delete an artist by their id
    # def delete(self, artist_id):
    #     self._connection.execute(
    #         'DELETE FROM artists WHERE id = %s', [artist_id])
    #     return None