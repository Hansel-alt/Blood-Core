from main import db, app 
from models import db, User

db.create_all(app=app)

bob = User(username='bob', email="bob@mail.com")
bob.set_password('bobpass')
db.session.add(bob)

print('database initialized!')