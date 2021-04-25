from main import db, app 

db.drop_all()
db.create_all(app=app)

print('database initialized!')