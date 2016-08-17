import uuid
from chirp import *
class Conversation:

    def __init__(self, message_id, is_private=False):
        self.chirp_id = message_id
        self.private = is_private
        self.chirps = list()
        self.obj_id = uuid.uuid4().int
