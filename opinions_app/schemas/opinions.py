from apiflask import Schema
from apiflask.fields import String
from marshmallow import validates, ValidationError



class AddOpinionSchema(Schema):
    title = String(required=True)
    text = String(required=True)
    source = String()

class OpinionOutputSchema(AddOpinionSchema):
    pass

class BlockOpinionSchema(Schema):
    reason = String(required=True)

    @validates("reason")
    def validate_reason(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Укажите причину блокировки")


