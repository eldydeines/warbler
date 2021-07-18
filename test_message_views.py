"""Message View tests."""

import os
from unittest import TestCase

from models import db, connect_db, Message, User

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

# Create our tables 
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test
app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User(username="testuser", 
                            email="test@test.com",
                            password="testuser",
                            image_url=None)
        self.testuser_id = self.testuser.id
        
        db.session.add(self.testuser)
        db.session.commit()

    def test_add_message(self):
        """Can user add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

    
    def test_messages_show(self):
        """Can we see a specific message that has been routed"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            #********** Setup ************#
            self.testmsg = Message(id=111,text="Test User Message", user_id=self.testuser.id )
            db.session.add(self.testmsg)
            db.session.commit()

            #********** Testing ************#
            resp = c.get(f'/messages/{self.testmsg.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User Message", html)

    def test_messages_destroy(self):
        """Check to see if new message is deleted"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            #********** Setup ************#
            self.testmsg = Message(id=112,text="Test User Message 2", user_id=self.testuser.id )
            db.session.add(self.testmsg)
            db.session.commit()

            #********** Testing ************#
            resp = c.post(f"/messages/{self.testmsg.id}/delete")

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one_or_none()
            self.assertIsNone(msg)
    
    def test_show_all_messages(self):
        """Check to see if all messages are shown"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            #********** Setup ************#
            self.testmsg1 = Message(id=111,text="Test User Message 1", user_id=self.testuser.id )
            db.session.add(self.testmsg1)
            self.testmsg2 = Message(id=112,text="Test User Message 2", user_id=self.testuser.id )
            db.session.add(self.testmsg2)
            db.session.commit()

            resp = c.get(f'/messages')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("111", html)
            self.assertIn("112", html)

    def test_message_like(self):
        """Check to see likes/unlikes are routed correctly"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
           
           #********** Setup ************#
            self.testmsg1 = Message(id=111,text="Test User Message 1", user_id=self.testuser.id )
            db.session.add(self.testmsg1)
            db.session.commit()

            #********** Testing ************#
            resp = c.post(f'/messages/111/{self.testuser.id}/like')

            self.assertEqual(resp.status_code, 302)
            
            


