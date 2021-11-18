from marshmallow import Schema, fields
from marshmallow.validate import OneOf, Length, Range



class MedicineSchema(Schema):
    id_medicine = fields.Integer(strict=True)
    name = fields.String(validate=Length(min=3, max=100))
    manufacturer = fields.String(validate=Length(min=3, max=100))
    price = fields.Integer(strict=True, validate=Range(min=0))
    in_stock = fields.Boolean(strict=True)
    demand = fields.Boolean(strict=True)
    in_stock_number = fields.Integer(strict=True, validate=Range(min=0))
    demand_number = fields.Integer(strict=True, validate=Range(min=0))


class UserSchema(Schema):
    id_user = fields.Integer(strict=True)
    login = fields.String( validate=Length(min=3, max=100))
    firstName = fields.String(validate=Length(min=3, max=100))
    lastName = fields.String(validate=Length(min=3, max=100))
    email = fields.String(validate=Length(min=3, max=100))
    password = fields.String(validate=Length(min=8, max=200))
    phone = fields.String(validate=Length(min=10, max=12))


class OrderSchema(Schema):
    id_order = fields.Integer(strict=True)
    id_medicine = fields.Integer(strict=True)
    id_user = fields.Integer(strict=True)
    amount = fields.Integer(strict=True)
    shipDate = fields.Date()
    status = fields.String(required=True)
    complete = fields.Boolean(default=False)
