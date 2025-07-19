import os, psycopg
from flask import g
from psycopg.rows import dict_row


class DatabaseConnection:
    # --- VVV REMOVE/CHANGE THESE VVV ---
    # These are good for local development, but on Render,
    # you'll primarily use the DATABASE_URL environment variable.
    DEV_DATABASE_NAME = "solo_bnb"
    TEST_DATABASE_NAME = "solo_bnb_test"
    # --- ^^^ REMOVE/CHANGE THESE ^^^ ---

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.connection = None # Initialize connection to None

    def connect(self):
        # Determine the database connection string based on environment
        # Prioritize DATABASE_URL from environment (for Render deployment)
        database_url = os.environ.get('DATABASE_URL')

        if database_url:
            # If DATABASE_URL is set (e.g., on Render), use it directly
            # psycopg automatically parses the full URL.
            conn_string = database_url
        else:
            # Fallback for local development
            # Use environment variable for local DB name if you have one, or fallback to constants
            db_name = os.environ.get('LOCAL_DB_NAME') or self.DEV_DATABASE_NAME
            if self.test_mode:
                db_name = os.environ.get('LOCAL_TEST_DB_NAME') or self.TEST_DATABASE_NAME

            conn_string = f"postgresql://localhost/{db_name}"
            # You might need to add user/password if your local setup requires it:
            # conn_string = f"postgresql://{os.environ.get('DB_USER', 'your_local_user')}:{os.environ.get('DB_PASSWORD', 'your_local_password')}@localhost/{db_name}"


        try:
            self.connection = psycopg.connect(
                conn_string,
                row_factory=dict_row
            )
        except psycopg.OperationalError as e:
            # Provide more specific error message based on the attempt
            db_info = f"'{conn_string}'"
            if not database_url:
                db_info += f" (Attempted local connection to {db_name})"
            raise Exception(f"Couldn't connect to the database {db_info}! Details: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred during database connection: {e}")


    def seed(self, sql_filename):
        self._check_connection()
        if not os.path.exists(sql_filename):
            raise Exception(f"File {sql_filename} does not exist")
        
        # It's better to read the SQL file as individual commands
        # because the seed.sql might contain multiple statements
        # separated by semicolons, and psycopg's execute might only
        # run the first one or throw an error.
        with open(sql_filename, "r") as f:
            sql_commands = f.read().split(';')
            with self.connection.cursor() as cursor:
                for command in sql_commands:
                    stripped_command = command.strip()
                    if stripped_command:
                        try:
                            cursor.execute(stripped_command)
                        except psycopg.Error as e:
                            # Log or handle errors for specific commands if necessary
                            print(f"Error executing SQL command during seed: {stripped_command[:100]}... Error: {e}")
                            # Decide whether to raise or continue based on your seeding philosophy
                            self.connection.rollback() # Rollback on individual error
                            raise # Re-raise to stop seeding on error
                self.connection.commit()


    def execute(self, query, params=[]):
        self._check_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description is not None:
                result = cursor.fetchall()
            else:
                result = None
            self.connection.commit() # Commit after each execute if not using explicit transactions
            return result

    CONNECTION_MESSAGE = 'DatabaseConnection.exec_params: Cannot run a SQL query as ' \
                         'the connection to the database was never opened. Did you ' \
                         'make sure to call first the method DatabaseConnection.connect` ' \
                         'in your app.py file (or in your tests)?'

    def _check_connection(self):
        # Also check if the connection is active/closed, not just None
        if self.connection is None or self.connection.closed:
            raise Exception(self.CONNECTION_MESSAGE)

    # This method is no longer needed to *determine* the name,
    # but the logic for test_mode is now in connect().
    # You can remove it or keep it as a helper if needed elsewhere.
    def _database_name(self):
        # This function might become redundant if all connections are from DATABASE_URL
        # or managed directly within connect().
        # However, for clarity in local dev, you can still return the name.
        if self.test_mode:
            return self.TEST_DATABASE_NAME
        else:
            return self.DEV_DATABASE_NAME

# This function integrates with Flask to create one database connection that
# Flask request can use. To see how to use it, look at example_routes.py
def get_flask_database_connection(app):
    # Use a new connection for each request for statelessness,
    # but store it on 'g' so it's only created once per request.
    if not hasattr(g, 'flask_database_connection') or g.flask_database_connection.connection is None or g.flask_database_connection.connection.closed:
        db_conn = DatabaseConnection(
            test_mode=((os.getenv('APP_ENV') == 'test') or (app.config.get('TESTING', False) == True))
        )
        db_conn.connect()
        g.flask_database_connection = db_conn
    return g.flask_database_connection