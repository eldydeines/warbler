"""User model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler"

from app import app, users_followers

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        #Setup user1, user2, and user3
        user1 = User.signup("fake_user1","faker1@faker.com","faker1pwd", None)
        self.user1_id = user1.id
        self.user1 = user1
        user2 = User.signup("fake_user2","faker2@faker.com","faker2pwd", None)
        self.user2_id = user2.id
        self.user2 = user2
        user3 = User.signup("fake_user3","faker3@faker.com","faker3pwd", None)
        self.user3_id = user3.id
        self.user3 = user3
        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages, no followers, not following and no likes
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(len(u.following), 0)
        self.assertEqual(len(u.likes), 0)

    def test_user_following(self):
        """Does user1 follow user2"""

        #Make user1 follow user2
        self.user1.following.append(self.user2)
        db.session.commit()

        #check following stats
        self.assertEqual(len(self.user1.following), 1)
        self.assertEqual(len(self.user2.followers), 1)

    def test_is_following(self):
        """Tesing model function is_following"""
        
        #Make user1 follow user2
        self.user1.following.append(self.user2)
        db.session.commit()

        #check class method
        self.assertTrue(self.user1.is_following(self.user2))
        self.assertFalse(self.user1.is_following(self.user3))

    def test_is_followed_by(self):
        """Tesing model function is_followed_by"""
        
        #Make user1 follow user2
        self.user1.following.append(self.user2)
        db.session.commit()

        #check class method
        self.assertTrue(self.user2.is_followed_by(self.user1))
        self.assertFalse(self.user3.is_following(self.user1))

    def test_user_signup_1(self):
        """Testing validation of form signup for user"""
        
        self.assertEqual(self.user1.username, "fake_user1")
        self.assertEqual(self.user1.email, "faker1@faker.com")
        self.assertNotEqual(self.user1.password, "faker1pwd")
        self.assertEqual(self.user1.image_url, None)
        self.assertIsNone(self.user1.header_image_url)

    def test_user_signup_2(self):
        """Testing validation of form signup for user"""
        
        #Not unique username should raise error
        invalid_user_1 = User.signup("fake_user1", "faker4@faker.com", "password", None)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
        #with exception need to rollback commit
        db.session.rollback()
        #Not unique email should raise error
        invalid_user_1 = User.signup("fake_user4", "faker1@faker.com", "password", None)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_authenticate(self):
        """Testing validation User.authentical"""

        #Send good info
        status_returned_user = User.authenticate("fake_user1", "faker1pwd")
        #Send bad info
        status_returned_bad_info = User.authenticate("fake_user1", "faker1")

        self.assertIs(self.user1, status_returned_user)
        self.assertFalse(status_returned_bad_info)
