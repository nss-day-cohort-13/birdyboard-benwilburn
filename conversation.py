import uuid
from chirp import *
class Conversation:

    def __init__(self, message_id):
        self.chirp_id = message_id
        self.obj_id = uuid.uuid4().int
