import uuid
import datetime

from app.main import db
from app.main.model.posts import Posts
from app.main.model.user import User

def save_new_post(data):
        user = User.query.filter_by(id=data['user_id']).first()
        if user:
            try:
                new_post = Posts(
                    title=data['title'],
                    description=data['description'],
                    content=data['content'],
                    user_id=data['user_id'],
                )
                save_changes(new_post)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully create new post.',
                }
                return response_object, 201
            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': 'can write new posts.',
                }
                return response_object, 409
        else:
            response_object = {
                'status': 'fail',
                'message': 'User not found. Please Log in.',
            }
            return response_object, 409

def get_all_posts():
    posts =Posts.query.all()
    print(posts)
    print(posts[1].user.username)
    return posts

def get_a_post_by_user(user_id):
    return Posts.query.filter_by(user_id=user_id).all()

def get_a_post_by_id(post_id):
    return Posts.query.get(post_id)

def save_changes(data):
    db.session.add(data)
    db.session.commit()

