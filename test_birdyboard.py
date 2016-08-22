import unittest
from birdyboard import *

class TestBirdyboard(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.birdyboard = Birdyboard()

    def test_users_is_a_list(self):
        self.assertIsInstance(self.birdyboard.users_directory, list)

    def test_private_chirps_is_a_list(self):
        self.assertIsInstance(self.birdyboard.private_chirps, list)

    def test_public_chirps_is_a_list(self):
        self.assertIsInstance(self.birdyboard.public_chirps, list)

    def test_current_user_is_none_by_default(self):
        self.assertIsNone(self.birdyboard.current_user)

if __name__ == '__main__':
    unittest.main()
