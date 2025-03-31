from flask import Flask, request, render_template, jsonify
import redis
from models import db, UserFavs
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Use environment variables for database and Redis connections
DB_USER = os.getenv('POSTGRES_USER', 'myuser')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost') 
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'mydatabase')

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

# PostgreSQL Connection URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()

# Initialize Redis
red = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), db=0)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route("/")
def main():
    return render_template('home.html')

@app.route("/add")
def add_wishlist():
    return render_template('add.html')

@app.route("/fetch")
def fetch_wishlist():
    return render_template('fetch.html')

@app.route("/save", methods=['POST'])
def save():
    username = request.form['username'].lower()
    place = request.form['place'].lower()
    food = request.form['food'].lower()
    user_data = red.hgetall(username)
    if user_data:
        # If user exists in Redis but not in DB, add data to the database
        record = UserFavs.query.filter_by(username=username).first()
        if not record:
            new_record = UserFavs(username=username, place=user_data[b'place'].decode(), food=user_data[b'food'].decode())
            db.session.add(new_record)
            db.session.commit()
        return render_template('add.html', user_exists=1, msg='(From Redis)', username=username, place=red.hget(username, "place").decode(), food=red.hget(username, "food").decode())
    
    # Check if user exists in the database
    record = UserFavs.query.filter_by(username=username).first()
    if record:
        red.hset(username, "place", record.place)
        red.hset(username, "food", record.food)
        return render_template('add.html', user_exists=1, msg='(From Database)', username=username, place=record.place, food=record.food)
    
    # If user does not exist in either Redis or Database, save new entry
    new_record = UserFavs(username=username, place=place, food=food)
    db.session.add(new_record)
    db.session.commit()

    red.hset(username, "place", place)
    red.hset(username, "food", food)

    return render_template('add.html', saved=1, username=username, place=place, food=food)

@app.route("/get", methods=['POST'])
def get():
    username = request.form['username'].lower()
    user_data = red.hgetall(username)

    if not user_data:
        record = UserFavs.query.filter_by(username=username).first()
        if not record:
            return render_template('fetch.html', no_record=1, msg=f"Record not yet defined for {username}")
        red.hset(username, "place", record.place)
        red.hset(username, "food", record.food)
        return render_template('fetch.html', get=1, msg="(From Database)", username=username, place=record.place, food=record.food)

    return render_template('fetch.html', get=1, msg="(From Redis)", username=username, place=user_data[b'place'].decode(), food=user_data[b'food'].decode())

@app.route("/keys", methods=['GET'])
def keys():
    records = UserFavs.query.all()
    names = [record.username.title() for record in records]
    return render_template('keys.html', usernames=names)

@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        username = request.form['username'].lower()
        new_place = request.form['place'].lower()
        new_food = request.form['food'].lower()

        record = UserFavs.query.filter_by(username=username).first()
        if not record:
            return render_template('edit.html', no_record=True, msg="No such user found.")

        record.place = new_place
        record.food = new_food
        db.session.commit()

        red.hset(username, "place", new_place)
        red.hset(username, "food", new_food)

        return render_template('edit.html', edited=True, msg="Wishlist updated successfully.")

    return render_template('edit.html')


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        username = request.form['username'].lower()

        record = UserFavs.query.filter_by(username=username).first()
        if not record:
            return render_template('delete.html', no_record=True, msg="No such user found.")

        db.session.delete(record)
        db.session.commit()
        red.delete(username)

        return render_template('delete.html', deleted=True, msg="Wishlist deleted successfully.")

    return render_template('delete.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

