from chaps import inject
from hopeit.actions import Action

from hopeit.models.message import Message


@inject('db_session')
class GetAllMessages(Action):

    def get_all_messages(self):
        return self.db_session.query(Message).filter(
            Message.user_id.is_(None)).order_by(Message.date.desc())

    def do(self):
        return {'messages': [{
            'id': m.id,
            'body': m.body,
            'message_type': m.message_type,
            'picture': m.picture,
            'date': str(m.date)
        } for m in self.get_all_messages()]}