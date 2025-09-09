from testapp import app, db
from testapp.models.employee import Employee

with app.app_context():
    db.create_all()

print("Database tables created!")
