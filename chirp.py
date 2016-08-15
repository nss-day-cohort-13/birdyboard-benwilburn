import uuid
from user import *
from conversation import *
class Chirp:

    def __init__(self,
                user_id,
                message,
                is_private=False,
                target=None):
        self.author = user_id
        self.chirp_message = message
        self.private = is_private
        self.recipient = target
        self.obj_id = uuid.uuid4().int
