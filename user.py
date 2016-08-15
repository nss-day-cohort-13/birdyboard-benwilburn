import uuid
class User:

    def __init__(self, fullname, username):
        self.full_name = fullname
        self.user_name = username
        self.obj_id = uuid.uuid4().int
