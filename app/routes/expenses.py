from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.expense_schema import ExpenseSchema
from app.services import expense_service
from app.utils.responses import success_response
from datetime import datetime

expenses_bp = Blueprint("expenses", __name__)

expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)


@expenses_bp.route("/", methods=["POST"])
@jwt_required()
def create_expense():
    user_id = get_jwt_identity()
    data = request.get_json()
    clean_data = expense_schema.load(data)
    expense = expense_service.create(clean_data, user_id)
    return success_response(expense_schema.dump(expense), 201)


@expenses_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_expenses():
    user_id = get_jwt_identity()
    category = request.args.get("category")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    expenses = expense_service.get_all(user_id, category, start_date, end_date)
    return success_response(expenses_schema.dump(expenses))


@expenses_bp.route("/<int:expense_id>", methods=["GET"])
@jwt_required()
def get_expense(expense_id):
    user_id = get_jwt_identity()
    expense = expense_service.get_by_id(expense_id, user_id)
    return success_response(expense_schema.dump(expense))


@expenses_bp.route("/<int:expense_id>", methods=["PUT"])
@jwt_required()
def update_expense(expense_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    clean_data = expense_schema.load(data, partial=True)
    expense = expense_service.update(expense_id, clean_data, user_id)
    return success_response(expense_schema.dump(expense))


@expenses_bp.route("/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):
    user_id = get_jwt_identity()
    expense_service.delete(expense_id, user_id)
    return success_response({"message": "Expense deleted successfully"})


@expenses_bp.route("/summary", methods=["GET"])
@jwt_required()
def monthly_summary():
    user_id = get_jwt_identity()
    summary = expense_service.monthly_summary(user_id)
    return success_response({
        "month": summary["month"],
        "total": summary["total"],
        "count": summary["count"],
        "expenses": expenses_schema.dump(summary["expenses"])
    })