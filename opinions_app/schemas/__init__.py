from apiflask import Schema
from apiflask.fields import String

class MessageOutputSchema(Schema):
    message = String()

from .auth import RegisterSchema, LoginSchema, TokenSchema, RefreshTokenSchema, ProfileSchema
from .opinions import AddOpinionSchema, OpinionOutputSchema, BlockOpinionSchema
from .admin import BlockUserSchema, UsersListSchema, OpinionsListSchema







