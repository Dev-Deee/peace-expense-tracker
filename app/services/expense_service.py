from app import db
from app.models.expense import Expense
from app.exceptions import NotFoundException, UnauthorizedException
from datetime import datetime, timezone


def create(data, user_id):
    expense = Expense(
        amount=data["amount"],
        category=data["category"],
        description=data.get("description"),
        date=data.get("date", datetime.now(timezone.utc)),
        user_id=user_id
    )
    db.session.add(expense)
    db.session.commit()
    return expense


def get_all(user_id, category=None, start_date=None, end_date=None):
    query = Expense.query.filter_by(user_id=user_id)

    if category:
        query = query.filter(Expense.category.ilike(f"%{category}%"))

    if start_date:
        query = query.filter(Expense.date >= start_date)

    if end_date:
        query = query.filter(Expense.date <= end_date)

    return query.all()


def get_by_id(expense_id, user_id):
    expense = Expense.query.get(expense_id)
    if not expense:
        raise NotFoundException("Expense not found")
    if expense.user_id != int(user_id):
        raise UnauthorizedException("You do not have access to this expense")
    return expense


def update(expense_id, data, user_id):
    expense = get_by_id(expense_id, user_id)

    if "amount" in data:
        expense.amount = data["amount"]
    if "category" in data:
        expense.category = data["category"]
    if "description" in data:
        expense.description = data["description"]
    if "date" in data:
        expense.date = data["date"]

    db.session.commit()
    return expense


def delete(expense_id, user_id):
    expense = get_by_id(expense_id, user_id)
    db.session.delete(expense)
    db.session.commit()


def monthly_summary(user_id):
    now = datetime.now(timezone.utc)
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    expenses = Expense.query.filter(
        Expense.user_id == int(user_id),
        Expense.date >= start_of_month
    ).all()

    total = 0
    for expense in expenses:
        total += expense.amount

    return {
        "month": now.strftime("%B %Y"),
        "total": total,
        "count": len(expenses),
        "expenses": expenses
    }