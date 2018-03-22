from . import db


class UserProfile(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    biography = db.Column(db.String(255))
    image = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    age = db.Column(db.String(80))
    profile_created_on = db.Column(db.String(80))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
