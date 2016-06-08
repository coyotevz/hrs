# -*- coding: utf-8 -*-

from marshmallow import Schema, fields, validates, ValidationError, post_load
from hrs.models import Employee
from hrs.utils.validators import validate_cuit


class EmployeeSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    birth_date = fields.Date(required=True)
    hire_date = fields.Date(required=True)
    cuil = fields.String(required=True)
    user_code = fields.Integer()
    file_no = fields.Integer()

    @validates('cuil')
    def validate_valid_unique_cuil(self, value):
        if not validate_cuit(value):
            raise ValidationError("CUIL field invalid.")
        exists = Employee.query.filter(Employee.cuil == value).first()
        if exists is not None:
            if self.context.get('employee_id', None) == exists.id:
                return True
            raise ValidationError("Employee CUIL must be unique.")
        return True

    @post_load
    def make_employee(self, data):
        if self.partial:
            return data
        return Employee(**data)
