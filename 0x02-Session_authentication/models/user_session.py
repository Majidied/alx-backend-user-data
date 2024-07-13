#!/usr/bin/env python3
""" Module of Session Authentication with expiration """
from models.base import Base


class UserSession(Base):
    """ User Session Class """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance """
        super().__init__(*args, **kwargs)

        user_id: str = kwargs.get('user_id')
        session_id: str = kwargs.get('session_id')

        if user_id is not None:
            self.user_id = user_id
        if session_id is not None:
            self.session_id = session_id
