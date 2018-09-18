
from .. import db, flask_bcrypt
import datetime
from app.main.model.user import User


class Posts(db.Model):
    """ Posts Model for storing user related details """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    like_number = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=False)

    user = db.relationship("User", foreign_keys=[user_id], backref="posts")

        
    def check_id(self, id):
        return self.id == id
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Post(%(id)s)>" % self.__dict__
