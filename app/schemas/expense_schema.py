from app import ma
from app.models.expense import Expense
from marshmallow import fields, validate


class ExpenseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Expense

    id = ma.auto_field(dump_only=True)
    amount = ma.auto_field(required=True, validate=validate.Range(min=0.01))
    category = ma.auto_field(required=True, validate=validate.Length(min=1, max=100))
    description = ma.auto_field()
    date = ma.auto_field()
    created_at = ma.auto_field(dump_only=True)
    user_id = ma.auto_field(dump_only=True)