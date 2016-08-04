import unittest
import uuid
from birdyboard import *

class Test_Chirp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.chirp = Chirp(1234,
                            "this is a chirp",
                            True,
                            4321)

    def test_self_chirp_is_a_chirp(self):
        self.assertIsInstance(self.chirp, Chirp)

    def test_chirp_author_value(self):
        self.assertIsInstance(self.chirp.author, int)
        self.assertEqual(self.chirp.author, 1234)

    def test_chirp_message_value(self):
        self.assertIsInstance(self.chirp.chirp_message, str)
        self.assertEqual(self.chirp.chirp_message, 'this is a chirp')

    def test_chirp_private_value(self):
        self.assertIsInstance(self.chirp.private, bool)
        self.assertEqual(self.chirp.private, True)

    def test_chirp_target_value(self):
        self.assertEqual(self.chirp.recipient, 4321)

    def test_chirp_id_type(self):
        self.assertEqual(type(self.chirp.message_id), uuid.UUID)


if __name__ == "__main__":
    unittest.main()
