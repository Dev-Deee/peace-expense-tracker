from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.user_schema import UserSchema
from app.services import user_authorization_service
from app.utils.responses import success_response

auth_bp = Blueprint("user_authorization", __name__)

user_schema = UserSchema()


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    clean_data = user_schema.load(data)
    user = user_authorization_service.register(clean_data)
    return success_response(user_schema.dump(user), 201)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    clean_data = user_schema.load(data, partial=("username",))
    result = user_authorization_service.login(clean_data)
    return success_response({
        "access_token": result["access_token"],
        "user": user_schema.dump(result["user"])
    }, 200)


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = user_authorization_service.get_user_by_id(user_id)
    return success_response(user_schema.dump(user))