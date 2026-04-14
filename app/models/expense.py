from app import db
from datetime import datetime, timezone


def get_current_time():
    return datetime.now(timezone.utc)


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.DateTime, nullable=False, default=get_current_time)
    created_at = db.Column(db.DateTime, default=get_current_time)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

