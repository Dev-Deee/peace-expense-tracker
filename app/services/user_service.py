from app import db, bcrypt
from app.models.user import User
from app.exceptions import NotFoundException, ConflictException, UnauthorizedException
from flask_jwt_extended import create_access_token


def register(data):
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        raise ConflictException("A user with this email already exists")

    existing_username = User.query.filter_by(username=data["username"]).first()
    if existing_username:
        raise ConflictException("This username is already taken")

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return user


def login(data):
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
        raise UnauthorizedException("Invalid email or password")

    access_token = create_access_token(identity=str(user.id))

    return {"access_token": access_token, "user": user}

def get_user_by_id(user_id):
    user = User.query.get(int(user_id))
    if not user:
        raise NotFoundException("User not found")
    return user