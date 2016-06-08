# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, abort

from sqlalchemy.exc import IntegrityError

from webargs.flaskparser import parser

from hrs.models import db, Employee
from hrs.schema import EmployeeSchema
from hrs.utils.rest import build_result


api = Blueprint('api', __name__, url_prefix='/api/v1')


def configure_api(app):
    app.register_blueprint(api)


@api.route('/employees')
def list_employees():
    q = Employee.query.order_by(Employee.file_no)
    return build_result(q, EmployeeSchema())


@api.route('/employees', methods=['POST'])
def new_employee():
    employee = parser.parse(EmployeeSchema(strict=True))
    db.session.add(employee)
    db.session.commit()
    return (build_result(employee, EmployeeSchema()), 201,
            {'Location': url_for('.get_employee', id=employee.id)})


@api.route('/employees/<int:id>')
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return build_result(employee, EmployeeSchema())


@api.route('/employees/<int:id>', methods=['PATCH'])
def update_employes(id):
    employee = Employee.query.get_or_404(id)
    args = parser.parse(EmployeeSchema(strict=True, partial=True,
                        context={'employee_id': employee.id}))
    for key, value in args.items():
        setattr(employee, key, value)
    db.session.commit()
    return build_result(employee, EmployeeSchema())


@api.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    try:
        db.session.commit()
    except IntegrityError:
        abort(409, description='Unable to delete employee')
    return '', 204
