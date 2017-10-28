import json
from datetime import datetime

from chaps import Inject

from hopeit.actions.create_payment import CreatePaymentAction
from hopeit.actions.get_user_payments import GetUserPaymentsAction
from hopeit.api.resources import CallAction, Resource
from hopeit.models import Goal, User
from hopeit.models.payment import Payment
from hopeit.models.message import Message
from hopeit.services.notifications.goal_completed import \
    GoalCompletedNotification
from hopeit.services.notifications.payment_confirm import (
    PaymentNotificationConfirm)
from hopeit.services.notifications.message import MessageNotification


class CreatePayment(Resource):
    on_post = CallAction(CreatePaymentAction)


class Collection(Resource):
    on_get = CallAction(GetUserPaymentsAction)


class GetPaymentStatus(Resource):
    db_session = Inject('db_session')

    def on_post(self, req, resp):
        data = json.dumps(
            str(req.stream.read(), "utf-8")).replace('%40', '@').split('&')
        dict_data = dict(
            s.split('=') for s in [a.replace('"', '') for a in data])

        user_id_from_description_data = int(
            dict_data['description'].replace('%3A', ':').split(':')[1])
        active_goal = self.db_session.query(Goal).filter(
            Goal.finished.is_(False),
            Goal.user_id == user_id_from_description_data).first()

        payment = Payment(
            user_id=user_id_from_description_data,
            goal_id=active_goal.id if active_goal else active_goal,
            operation_number=dict_data['operation_number'],
            operation_type=dict_data['operation_type'],
            operation_status=dict_data['operation_status'],
            operation_amount=float(dict_data['operation_amount']),
            operation_currency=dict_data['operation_currency'],
            description=dict_data['description'],
            email=dict_data['email'],
            channel=int(dict_data['channel']),
            signature=dict_data['signature']
        )
        message = Message(
            user_id=user_id_from_description_data,
            message_type=Message.MESSAGE_TYPE_PAYMENT,
            body='Płatność została zrealizowana.',
        )
        self.db_session.add(payment)
        self.db_session.add(message)

        self.db_session.flush()

        user = self.db_session.query(User).filter(
            User.id == user_id_from_description_data).first()
        device_id = user.device
        if active_goal and active_goal.balance >= active_goal.target:
            active_goal.finished = True
            GoalCompletedNotification().send_single_device(device_id)
            Message(
                user_id=user.id,
                body="Gratulacje! Ukończyłeś założony cel!",
                picture='')
            MessageNotification().send_single_device(device_id)

        PaymentNotificationConfirm().send_single_device(
            device_id, payment.operation_amount)
        MessageNotification().send_single_device(device_id)

        resp.body = 'OK'
