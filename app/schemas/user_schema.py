from app import ma
from app.models.user import User
from marshmallow import fields, validate


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(required=True, validate=validate.Length(min=3, max=80))
    email = ma.auto_field(required=True, validate=validate.Email())
    password = fields.String(required=True, validate=validate.Length(min=6), load_only=True)
    created_at = ma.auto_field(dump_only=True)