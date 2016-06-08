# -*- coding: utf-8 -*-

import json
from hrs.application import create_app
from nbs.config import TestingConfig
from nbs.models import db


def json_data(resp):
    return json.loads(resp.data.decode('utf-8') if len(resp.data) else '{}')


class TestCase(object):
    """Base class for test which use a Flask application

    The Flask test client can be accesed at ``self.client``. The Flask
    application itself is accesible at ``self.app``.
    """

    def setup(self):
        self.app = create_app(config=TestingConfig)
        self._app_context = self.app.app_context()
        self._app_context.push()
        self.db = db
        self.db.create_all()

    def teardown(self):
        self.db.drop_all()
        self._app_context.pop()
        self.app = None


class APITestCase(TestCase):

    def setup(self):
        super().setup()
        self.client = self.app.test_client()

    def teardown(self):
        self.client = None
        super().teardown()

    def get(self, *args, **kwargs):
        rv = self.client.get(*args, **kwargs)
        assert rv.mimetype == 'application/json'
        return rv, json_data(rv)

    def post(self, *args, **kwargs):
        rv = self.client.post(*args, **kwargs)
        assert rv.mimetype == 'application/json'
        return rv, json_data(rv)

    def path(self, *args, **kwargs):
        rv = self.client.patch(*args, **kwargs)
        assert rv.mimetype == 'application/json'
        return rv, json_data(rv)

    def delete(self, *args, **kwargs):
        rv = self.client.delete(*args, **kwargs)
        assert rv.mimetype == 'application/json'
        return rv, json_data(rv)


class DBTestCase(TestCase):
    """Base class for tests that involves database operations"""

    def add(self, thing):
        self.db.session.add(thing)

    def add_all(self, things):
        self.db.session.add_all(things)

    def commit(self):
        self.db.sesssion.commit()

    def add_commit(self, thing):
        self.db.session.add(thing)
        self.db.session.commit()
