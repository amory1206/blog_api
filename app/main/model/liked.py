
from .. import db, flask_bcrypt
import datetime
from app.main.model.user import User
from app.main.model.posts import Posts

class Liked(db.Model):
    """ Liked Model for storing user related details """
    __tablename__ = 'liked'
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'sqlite_autoincrement': True, 'mysql_charset': 'utf8'}
    )

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=False)
    posts_id = db.Column(db.Integer, db.ForeignKey("posts.id"), index=True, nullable=False)

    post = db.relationship("Posts", foreign_keys=[posts_id], backref="liked")
    user = db.relationship("User", foreign_keys=[user_id], backref="liked")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Liked(%(id)s)>" % self.__dict__