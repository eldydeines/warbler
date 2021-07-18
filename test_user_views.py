"""User View tests."""

import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

# Create our tables 
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test
app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()
        Message.query.delete()
        Likes.query.delete()

        #Setup test user
        self.testuser = User(username="testuser", 
                            email="test@test.com",
                            password="testuser",
                            image_url=None)
        self.testuser_id = self.testuser.id
        
        db.session.add(self.testuser)

        self.testuser2 = User(username="testuser2", 
                            email="tes2t@test.com",
                            password="testuser2",
                            image_url=None)
        self.testuser2_id = self.testuser2.id
        db.session.add(self.testuser2)
        db.session.commit()
        self.client = app.test_client()
    
    def test_list_users(self):
        """Can we see user"""
        with app.test_client() as c:
            resp = c.get("/users")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.testuser.username, html)
            self.assertIn(self.testuser2.username, html)

    def test_users_show(self):
        """Can user sign up?"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f"/users/{self.testuser.id}")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.testuser.username, html)

    def test_show_likes(self):
        """Show likes of said user"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            #setup data
            self.testmsg = Message(id=112,text="Test User Message 2", user_id=self.testuser.id )
            db.session.add(self.testmsg)
            db.session.commit()
            self.testlike = Likes(user_id=self.testuser.id, message_id=self.testmsg.id)
            db.session.add(self.testlike)
            db.session.commit()

            resp = c.get(f"/users/{self.testuser.id}/likes")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User Message 2", html)


    def test_show_following(self):
        """Show who the user is following"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            #setup data
            following = Follows(user_following_id=self.testuser_id, 
                                user_being_followed_id=self.testuser2_id)
            user_following = following.user_following_id
            db.session.commit()

            resp = c.get(f"/users/{self.testuser.id}/following")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{user_following}', html)

    def test_show_followers(self):
        """Show who is following the user"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            #setup data
            following = Follows(user_following_id=self.testuser_id, 
                                user_being_followed_id=self.testuser2_id)
            being_followed = following.user_being_followed_id
            db.session.commit()

            resp = c.get(f"/users/{self.testuser.id}/following")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{being_followed}', html)

    def test_profile(self):
        """Check if user profile displayed"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get("/users/profile")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

    def test_delete_user(self):
        """Check if user deleted"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/users/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location,"http://localhost/signup")




