import os
from flask import Flask, request, render_template, redirect, url_for, session, flash
from lib.database_connection import get_flask_database_connection
from lib.models.user import User
from lib.repos.user_repo import UserRepo
from lib.models.listing import Listing
from lib.repos.listing_repo import ListingRepo


# Create a new Flask app
app = Flask(__name__)

app.secret_key = 'secret_key'

# === Landing Page === #

# @app.route('/', methods=['GET'])
# def get_homepage():
#     return render_template('index.html')

# === User Routes === #

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

@app.route('/register', methods=['GET'])
def get_new_user():
    return render_template('users/new.html')

@app.route('/users', methods=['POST'])
def create_user():
    connection = get_flask_database_connection(app)
    repo = UserRepo(connection)
    
    username = request.form['username']
    email = request.form['email']
    password_hash = request.form['password_hash']
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    user = User(None, username, email, password_hash, first_name, last_name)

    if not user.is_valid():
        return render_template('users/new.html', user=user, errors=user.generate_errors()), 400

    user = repo.create(user)
    
    session['username'] = user.username
    session['user_id'] = user.id
    session['user_email'] = user.email
    
    return redirect(f"/users/{user.id}")

@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    connection = get_flask_database_connection(app)
    repo = UserRepo(connection)
    repo.delete(id)
    
    if session.get('username'):
        session.pop('username', None)
    if session.get('user_id'):
        session.pop('user_id', None)
    if session.get('first_name'):
        session.pop('first_name', None)
    if session.get('user_email'):
        session.pop('user_email', None)
        
    return redirect(url_for('get_all_users'))

@app.route('/login', methods=['GET'])
def show_log_in():
    return render_template('users/login.html')

@app.route('/login', methods=['POST'])
def log_in():
    connection = get_flask_database_connection(app)
    repo = UserRepo(connection)
    
    username = request.form['username']
    password = request.form['password_hash']
    
    users = repo.all()
    
    for user in users:
        if user.username == username and user.password_hash == password:
            session['user_id'] = user.id
            session['first_name'] = user.first_name
            return redirect(url_for('get_all_listings'))
    
    return render_template('users/login.html')
    
    

@app.route('/logout', methods=['GET'])
def log_out():
    if session.get('username'):
        session.pop('username', None)
    if session.get('user_id'):
        session.pop('user_id', None)
    if session.get('first_name'):
        session.pop('first_name', None)
    if session.get('user_email'):
        session.pop('user_email', None)
    return redirect(url_for('get_all_listings'))

# === Listing Routes === #

@app.route('/', methods=['GET'])
@app.route('/listings', methods=['GET'])
def get_all_listings():
    connection = get_flask_database_connection(app)
    repo = ListingRepo(connection)
    listings = repo.all_with_details()
    return render_template('listings/index.html', listings=listings)

@app.route('/listings/<int:id>', methods=['GET'])
def get_single_listing(id):
    connection = get_flask_database_connection(app)
    repo = ListingRepo(connection)
    listing = repo.find_by_id_with_details(id)
    return render_template('listings/show.html', listing=listing)

@app.route('/listings/new', methods=['GET'])
def get_new_listing():
    return render_template('listings/new.html')

@app.route('/listings', methods=['POST'])
def create_listing():
    connection = get_flask_database_connection(app)
    repo = ListingRepo(connection)
    
    host_id = request.form['host_id']
    title = request.form['title']
    description = request.form['description']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    price_per_night = request.form['price_per_night']
    max_guests = request.form['max_guests']
    image_urls = []
    image_urls.append(request.form['img_url_1'])
    image_urls.append(request.form['img_url_2'])
    image_urls.append(request.form['img_url_3'])

    listing = Listing(None, host_id, title, description, address, city, state, country, price_per_night, max_guests, None, None, None, image_urls)

    if not listing.is_valid():
        return render_template('listings/new.html', listing=listing, errors=listing.generate_errors()), 400

    listing = repo.create(listing)
    return redirect(f"/listings/{listing.id}")

@app.route('/listings/<int:id>/delete', methods=['POST'])
def delete_listing(id):
    connection = get_flask_database_connection(app)
    repo = ListingRepo(connection)
    repo.delete(id)

    return redirect(url_for('get_all_listings'))



# ================================================================

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
