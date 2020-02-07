#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Stock
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='dickpanshu', email="dickpanshu@dickpanshu.com")
        u.set_password('dick')
        self.assertFalse(u.check_password('vagina'))
        self.assertTrue(u.check_password('dick'))


    def test_add_stocks(self):
        # create four users
        u1 = User(username='Chunky', email='chunky@example.com')
        u2 = User(username='Brad', email='brad@example.com')
        u3 = User(username='lundfakir', email='lundfakir@example.com')
        u4 = User(username='boobs', email='boobs@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four stocks
        
        s1 = Stock(name="Stock1", price=500)
        s2 = Stock(name="Stock2", price=600)
        s3 = Stock(name="Stock3", price=700)

        db.session.add_all([s1, s2, s3])
        db.session.commit()

        # buy the stocks
        u1.add_stock(s1, 10)  # spend all 5000 for 10 s1
        u1.add_stock(s1, -5)  # sell 5 stocks to gain 2500 money
        u1.add_stock(s1, 10)  # try to buy more stocks than money left
        u1.add_stock(s1, -10)  # try to sell more stocks than bought
        u1.add_stock(s2, 2)

        u2.add_stock(s1)
        u2.add_stock(s2)
        u2.add_stock(s3)
        u2.add_stock(s1, -1)  # remove the stockitem completely from tables

        u3.add_stock(s2, -3)  # try to sell stock which in not purchased

        db.session.commit()

        u1_stocks = u1.stocks
        u2_stocks = u2.stocks
        u3_stocks = u3.stocks
        u1_s1_count = u1.stock_items.filter_by(stock=s1).first().quantity
        self.assertEqual(1300, u1.money)
        self.assertEqual(3700, u2.money)
        self.assertEqual(5000, u3.money)
        self.assertEqual(u1_stocks, [s1, s2])
        self.assertEqual(u2_stocks, [s2, s3])
        self.assertEqual(u3_stocks, [])
        self.assertEqual(u1_s1_count, 5)

if __name__ == '__main__':
    unittest.main(verbosity=2)
