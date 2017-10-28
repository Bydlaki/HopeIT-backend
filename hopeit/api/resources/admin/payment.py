from hopeit.actions.get_all_payments import GetAllPaymentsAction
from hopeit.api.hooks.authorization import authorize_user
from hopeit.api.resources import Resource, CallAction


class Collection(Resource):
    on_get = authorize_user(CallAction(GetAllPaymentsAction))
