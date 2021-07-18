"""Message model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler"

from app import app, users_followers

db.create_all()

class MessageModelTestCase(TestCase):
    """Test views for messages"""

    def setUp(self):
        """Create test client, add sample data."""
    
        #Setup user1, user2, and user3
        user1 = User.signup("fake_user1","faker1@faker.com","faker1pwd", None)
        self.user1_id = user1.id
        self.user1 = user1
        user2 = User.signup("fake_user2","faker2@faker.com","faker2pwd", None)
        self.user2_id = user2.id
        self.user2 = user2

        #Setup messages for user1
        user1_msg1 = Message(text="Test 1 Message for User 1")
        self.user1_msg1_id = user1_msg1.id
        self.user1_msg1 = user1_msg1
        self.user1.messages.append(self.user1_msg1_id)

        user1_msg2 = Message(text="Test 2 Message for User 1")
        self.user1_msg2_id = user1_msg2.id
        self.user1_msg2 = user1_msg2
        self.user1.messages.append(self.user1_msg2_id)
        self.client = app.test_client()

    def test_message_model(self):
        """Does basic model work?"""

        test_msg = Message(text="Test Message for User 1")
        test_msg_id = test_msg.id
        self.test_msg = test_msg
        self.user1.messages.append(test_msg)

        # User should have no messages, no followers, not following and no likes
        self.assertEqual(self.test_msg.id, test_msg_id)
        self.assertEqual(self.test_msg.text, "Test Message for User 1")
    
    
    def test_message_user_linkage(self):
        """Does basic model work?"""

        test_msg = Message(text="Test Message for User 1")
        test_msg_id = test_msg.id
        self.user1.messages.append(test_msg)

        # User should have no messages, no followers, not following and no likes
        self.assertEqual(len(self.user1.messages), 3)
        self.assertIn(test_msg, self.user1.messages)

    def test_message_add_to_user(self):
        """Does message pair up with the correct user"""
        test_msg = Message(text="Test Message for User 1 - Round 1", user_id=self.user1_id)

        # User1 should have new message
        self.assertEqual(test_msg.user_id, self.user1_id)
        # User2 should have no messages
        self.assertEqual(len(self.user2.messages), 0)
      