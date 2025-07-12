from lib.models.user import User

class UserRepo:
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all users
    def all(self):
        rows = self._connection.execute(
            """
            SELECT * from users
            """
            )
        users = []
        for row in rows:
            user = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                password_hash=row['password_hash'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            users.append(user)
        return users

    # Find a single user by their id
    def find(self, user_id):
        rows = self._connection.execute(
            """
            SELECT * from users WHERE id = %s
            """
            , [user_id])
        row = rows[0]
        return User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                password_hash=row['password_hash'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )

    # Create a new user
    def create(self, user):
        rows = self._connection.execute(
            """
            INSERT INTO users (username, email, password_hash, first_name, last_name) 
            VALUES (%s, %s, %s, %s, %s) RETURNING id
            """
            , [user.username, user.email, user.password_hash, user.first_name, user.last_name])
        new_id = rows[0]['id']
        return self.find(new_id)

    # Delete a user by their id
    def delete(self, user_id):
        self._connection.execute(
            """
            DELETE FROM users WHERE id = %s
            """
            , [user_id])
        return None