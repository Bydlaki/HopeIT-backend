import sqlalchemy as sq
from sqlalchemy.orm import relationship

from hopeit.database import Base


class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    username = sq.Column(sq.String)
    device = sq.Column(sq.String)

    goals = relationship("Goal", back_populates="user")

    def __repr__(self):
        return f'<User id={self.id} username={self.username}>'