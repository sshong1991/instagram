from django.db import IntegrityError
from django.test import TransactionTestCase

from utils.test.member import make_dummy_users


class MyUserModelTest(TransactionTestCase):
    def test_following(self):
        users = make_dummy_users()

        users[0].follow(users[1])
        users[0].follow(users[2])
        users[0].follow(users[3])

        users[1].follow(users[2])
        users[1].follow(users[3])

        users[2].follow(users[3])

        self.assertIn(users[1], users[0].following.all())
        self.assertIn(users[2], users[0].following.all())
        self.assertIn(users[3], users[0].following.all())

        self.assertIn(users[2], users[1].following.all())
        self.assertIn(users[3], users[1].following.all())

        self.assertIn(users[3], users[2].following.all())

        # 반대로 follower를 가진 유저는 follower_set 역참조 이름으로
        self.assertIn(users[0], users[3].follower_set.all())
        self.assertIn(users[1], users[3].follower_set.all())
        self.assertIn(users[2], users[3].follower_set.all())

        self.assertIn(users[0], users[2].follower_set.all())
        self.assertIn(users[1], users[2].follower_set.all())

        self.assertIn(users[0], users[1].follower_set.all())

    def test_following_duplicate(self):
        users = make_dummy_users()

        users[0].follow(users[1])

        with self.assertRaises(IntegrityError):
            users[0].follow(users[1])

        self.assertEqual(users[0].following.count(), 1)
        self.assertEqual(users[1].follower_set.count(), 1)

    def test_unfollow(self):
        users = make_dummy_users()
        users[0].follow(users[1])
        users[0].follow(users[2])
        users[0].follow(users[3])

        users[0].unfollow(users[1])
        self.assertEqual(users[0].following.count(), 2)

        users[0].unfollow(users[2])
        self.assertEqual(users[0].following.count(), 1)

        users[0].unfollow(users[3])
        self.assertEqual(users[0].following.count(), 0)
