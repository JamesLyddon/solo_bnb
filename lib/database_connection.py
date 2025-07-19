import os, psycopg
from flask import g
from psycopg.rows import dict_row

class DatabaseConnection:
    DEV_DATABASE_NAME = "solo_bnb"
    TEST_DATABASE_NAME = "solo_bnb_test"
    SEED_FILE_PATH = "seeds/bnb_seed.sql" # <--- Define your seed file path here

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.connection = None

    def connect(self):
        database_url = os.environ.get('DATABASE_URL')

        if database_url:
            conn_string = database_url
        else:
            db_name = os.environ.get('LOCAL_DB_NAME') or self.DEV_DATABASE_NAME
            if self.test_mode:
                db_name = os.environ.get('LOCAL_TEST_DB_NAME') or self.TEST_DATABASE_NAME
            local_db_user = os.environ.get('DB_USER', 'james')
            local_db_password = os.environ.get('DB_PASSWORD', '')
            conn_string = f"postgresql://{local_db_user}:{local_db_password}@localhost:5432/{db_name}"

        try:
            self.connection = psycopg.connect(
                conn_string,
                row_factory=dict_row
            )
            # --- VVV ADD THIS BLOCK VVV ---
            # Attempt to seed the database only if it's not in test mode
            # and if the tables don't already exist.
            if not self.test_mode: # Do not seed the test database this way
                self._initial_seed_if_needed()
            # --- ^^^ ADD THIS BLOCK ^^^ ---

        except psycopg.OperationalError as e:
            db_info = f"'{conn_string}'"
            if not database_url:
                db_info += f" (Attempted local connection to {db_name})"
            raise Exception(f"Couldn't connect to the database {db_info}! Details: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred during database connection: {e}")

    # Helper to check if tables exist (e.g., if 'users' table exists)
    def _tables_exist(self) -> bool:
        try:
            with self.connection.cursor() as cursor:
                # Query information_schema to check for a specific table (e.g., 'users')
                # This is a robust way to check if schema is already applied.
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT 1
                        FROM information_schema.tables
                        WHERE table_schema = 'public' AND table_name = 'users'
                    );
                """)
                return cursor.fetchone()['exists']
        except psycopg.Error as e:
            # If this check itself fails, it might indicate a connection issue
            # or a permission problem even before table existence.
            print(f"Warning: Could not check for existing tables: {e}")
            return False # Assume tables don't exist, or be cautious

    def _initial_seed_if_needed(self):
        if not self._tables_exist():
            print(f"No existing tables found. Seeding database with {self.SEED_FILE_PATH}...")
            try:
                self.seed(self.SEED_FILE_PATH)
                print("Database seeded successfully during initial connection.")
            except Exception as e:
                print(f"CRITICAL ERROR: Failed to seed database with {self.SEED_FILE_PATH}: {e}")
                # Depending on how critical this is, you might re-raise or sys.exit()
                # sys.exit(1) # Consider exiting if app can't function without schema
        else:
            print("Database tables already exist. Skipping seeding.")

    def seed(self, sql_filename):
        self._check_connection()
        if not os.path.exists(sql_filename):
            raise Exception(f"File {sql_filename} does not exist")

        with open(sql_filename, "r") as f:
            sql_commands = f.read().split(';')
            with self.connection.cursor() as cursor:
                for command in sql_commands:
                    stripped_command = command.strip()
                    if stripped_command:
                        try:
                            cursor.execute(stripped_command)
                        except psycopg.Error as e:
                            # Log and roll back the current transaction if a command fails
                            print(f"Error executing SQL command during seed: {stripped_command[:100]}... Error: {e}")
                            self.connection.rollback()
                            raise # Re-raise to stop the seeding process on first error
                self.connection.commit() # Commit all changes from the seed file if successful

    def execute(self, query, params=[]):
        self._check_connection()
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, params)
                if cursor.description is not None:
                    result = cursor.fetchall()
                else:
                    result = None
                self.connection.commit()
                return result
            except psycopg.Error as e:
                self.connection.rollback() # Rollback on error for execute calls
                raise # Re-raise the exception

    CONNECTION_MESSAGE = 'DatabaseConnection: Cannot run a SQL query as ' \
                         'the connection to the database was never opened or is closed. ' \
                         'Did you make sure to call `connect()` first?'

    def _check_connection(self):
        if self.connection is None or self.connection.closed:
            raise Exception(self.CONNECTION_MESSAGE)

    def _database_name(self):
        if self.test_mode:
            return self.TEST_DATABASE_NAME
        else:
            return self.DEV_DATABASE_NAME

# The get_flask_database_connection function remains the same
def get_flask_database_connection(app):
    if not hasattr(g, 'flask_database_connection') or g.flask_database_connection.connection is None or g.flask_database_connection.connection.closed:
        db_conn = DatabaseConnection(
            test_mode=((os.getenv('APP_ENV') == 'test') or (app.config.get('TESTING', False) == True))
        )
        try:
            db_conn.connect()
            g.flask_database_connection = db_conn
        except Exception as e:
            # Re-raise the error here so Flask catches it and displays 500
            # for the user, and you see the traceback in logs.
            raise RuntimeError(f"Failed to establish or seed database connection: {e}")
    return g.flask_database_connection