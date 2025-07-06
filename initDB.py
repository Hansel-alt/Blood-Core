from main import db, app
from models import User

with app.app_context():
    db.create_all()

    # Only add bob if he doesn't already exist
    if not User.query.filter_by(email='bob@mail.com').first():
        bob = User(username='bob', email='bob@mail.com')
        bob.set_password('bobpass')
        db.session.add(bob)
        db.session.commit()
        print("Added bob to the database.")
    else:
        print("User bob@mail.com already exists.")


print('database initialized!')
