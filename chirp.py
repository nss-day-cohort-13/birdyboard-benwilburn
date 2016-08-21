import uuid
import time
from user import *
from conversation import *
class Chirp:

    def __init__(self,
                user_id,
                message,
                target=None):
        self.author = user_id
        self.chirp_message = message
        self.recipient = target
        self.obj_id = uuid.uuid4().int
        self.time_stamp = time.strftime("%m-%d-%Y %H:%M")

    def __str__(self):
        return self.chirp_message
