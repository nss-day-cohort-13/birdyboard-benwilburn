import unittest
import uuid
from birdyboard import *

class Test_Chirp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.chirp = Chirp(1234, "this is a chirp", 4321, True, None)

    def test_chirp_exists(self):
        self.assertTrue(self.chirp)

    def test_chirp_author_value(self):
        self.assertIsInstance(self.chirp.author, int)
        self.assertEqual(self.chirp.author, 1234)

    def test_chirp_message_value(self):
        self.assertIsInstance(self.chirp.message, str)
        self.assertEqual(self.chirp.message, 'this is a chirp')

    def test_chirp_private_value(self):
        self.assertIsInstance(self.chirp.private, bool)
        self.assertEqual(self.chirp.private, True)

    def test_chirp_target_value(self):
        self.assertEqual(self.chirp.target, None)

if __name__ == "__main__":
    unittest.main()
