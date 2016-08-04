import unittest
import uuid
from birdyboard import *

class Test_User(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.user = User('Ben Wilburn',
                        'bwilburn',
                        self.person_id)

    def test_user_full_name_value(self):
        self.assertIsInstance(self.user.full_name, str)
        self.assertEqual(self.user.full_name, 'Ben Wilburn')

    def test_user_name_value(self):
        self.assertIsInstance(self.user.user_name, str)
        self.assertEqual(self.user.username, 'bwilburn')

    def test_user_id_type(self):
        self.assertEqual(type(self.user.user_id), uuid.UUID)
