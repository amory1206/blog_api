import uuid
import datetime

from app.main import db
from app.main.model.posts import Posts
from app.main.model.user import User
from app.main.model.liked import Liked

def save_new_liked(data):
        user = User.query.get(data['user_id']).first()
        post = Posts.query.get(data['post_id']).first()
        if user and post:
            liked = Liked.query.filter_by(user_id=data['user_id'], posts_id = data['post_id']).first()
            if liked:
                print(liked)
                delete(liked)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully unlike.',
                }
                return response_object, 201
            else:
                try:
                    new_like = Liked(
                        user_id=data['user_id'],
                        posts_id=data['post_id'],
                    )
                    save_changes(new_like)
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully like.',
                    }
                    return response_object, 201
                except Exception as e:
                    response_object = {
                        'status': 'fail',
                        'message': 'can like.',
                    }
                    return response_object, 409
        else:
            response_object = {
                'status': 'fail',
                'message': 'User not found. || post not found Please Log in.',
            }
            return response_object, 409


def get_a_liked_by_user(user_id):
    return Liked.query.filter_by(user_id=user_id).all()

def get_a_liked_by_post(posts_id):
    return Liked.query.filter_by(posts_id=posts_id).all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def delete(data):
    db.session.delete(data)
    db.session.commit()
