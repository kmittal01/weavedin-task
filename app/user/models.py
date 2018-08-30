from app.extensions import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.GUID(), primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(256))
    modified_by = db.Column(db.GUID())
    modified_on = db.Column(db.DateTime)
    created_by = db.Column(db.GUID())
    created_at = db.Column(db.DateTime)

    def __getitem__(self, item):
        return getattr(self, item)

