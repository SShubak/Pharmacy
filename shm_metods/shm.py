from marshmallow import Schema, fields
from marshmallow.validate import OneOf, Length, Range


class CategorySchema(Schema):
    id_category = fields.Integer(strict=True)
    name_category = fields.String(validate=Length(min=3, max=100))


class MedicineSchema(Schema):
    id_medicine = fields.Integer(strict=True)
    name_category = fields.String(validate=Length(min=3, max=100))
    id_category = fields.Integer(strict=True)
    manufacturer = fields.String(validate=Length(min=3, max=100))
    price = fields.Integer(strict=True, validate=Range(min=0))
    in_stock = fields.Boolean(strict=True)
    demand = fields.Boolean(strict=True)
    in_stock_number = fields.Integer(strict=True, validate=Range(min=0))
    demand_number = fields.Integer(strict=True, validate=Range(min=0))


class UserSchema(Schema):
    id_user = fields.Integer(strict=True)
    username = fields.String(required=True, validate=Length(min=3, max=100))
    firstName = fields.String(validate=Length(min=3, max=100))
    lastName = fields.String(validate=Length(min=3, max=100))
    email = fields.String(validate=Length(min=3, max=100))
    password = fields.String(required=True, validate=Length(min=8, max=100))
    phone = fields.String(validate=Length(min=10, max=12))


class OrderSchema(Schema):
    id_order = fields.Integer(strict=True)
    id_medicines = fields.Integer(strict=True)
    id_user = fields.Integer(strict=True)
    shipDate = fields.DateTime()
    status = fields.String(required=True, validate=OneOf("placed", "approved", "delivered"))
    complete = fields.Boolean(default=False)
