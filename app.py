import os
from flask import Flask, request, render_template, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.models.user import User
from lib.repos.user_repo import UserRepo


# Create a new Flask app
app = Flask(__name__)

# === User Routes Here === #

@app.route('/users', methods=['GET'])
def get_all_users():
    connection = get_flask_database_connection(app)
    repo = UserRepo(connection)
    users = repo.all()
    return render_template('users/index.html', users=users)

@app.route('/users/<int:id>', methods=['GET'])
def get_single_user(id):
    connection = get_flask_database_connection(app)
    repo = UserRepo(connection)
    user = repo.find(id)
    return render_template('users/show.html', user=user)

@app.route('/users/new', methods=['GET'])
def get_new_user():
    return render_template('users/new.html')

@app.route('/users', methods=['POST'])
def create_user():
    # Set up the database connection and repository
    connection = get_flask_database_connection(app)
    repo = UserRepo(connection)
    # Get the fields from the request form
    username = request.form['username']
    email = request.form['email']
    password_hash = request.form['password_hash']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    # Create a book object
    user = User(None, username, email, password_hash, first_name, last_name)
    # Check for validity and if not valid, show the form again with errors
    if not user.is_valid():
        return render_template('users/new.html', user=user, errors=user.generate_errors()), 400
    # Save the book to the database
    user = repo.create(user)
    # Redirect to the book's show route to the user can see it
    return redirect(f"/users/{user.id}")

@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_book(id):
    connection = get_flask_database_connection(app)
    repo = UserRepo(connection)
    repo.delete(id)

    return redirect(url_for('get_all_users'))





# ================================================================

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
