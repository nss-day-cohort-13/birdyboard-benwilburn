import unittest
import uuid
from birdyboard import *

class Test_Conversation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.conversation = Conversation(1234)

    def test_self_conversation_is_a_conversation(self):
        self.assertIsInstance(self.conversation, Conversation)

    def test_chirp_id_value(self):
        self.assertEqual(self.conversation.chirp_id, 1234)

    def test_chirp_id_type(self):
        self.assetEqual(type(self.conversation.conversation_id), uuid.UUID)
