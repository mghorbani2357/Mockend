import json
import time
from unittest import TestCase
from mockend import config, app


class TestEndPoints(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_simple_endpoint(self):
        config.update({
            "users": {
                "get": {
                    "response": {
                        "user_ids": [1, 2, 3]
                    }
                }
            }
        })

        self.assertEqual(self.app.get('/users').data, b'{"user_ids": [1, 2, 3]}')

    def test_nested_endpoints(self):
        config.update({
            "users": {
                "JohnDoe": {
                    "get": {
                        "response": {
                            "name": "John Doe",
                            "email": "J.Doe@test.com"
                        }
                    }
                }
            }
        })

        response = json.dumps({
            "name": "John Doe",
            "email": "J.Doe@test.com"
        }).encode('utf-8')

        self.assertEqual(self.app.get('/users/JohnDoe').data, response)

    def test_delay_endpoint(self):
        config.update({
            "users": {
                "get": {
                    "delay": 0.1,
                    "response": {
                        "user_ids": [1, 2, 3]
                    }
                }
            }
        })

        run_time = time.time()

        self.assertEqual(self.app.get('/users').data, b'{"user_ids": [1, 2, 3]}')
        self.assertGreaterEqual(0.1, time.time() - run_time)

    def test_chuck_response(self):
        config.update({
            "users": {
                "get": {
                    "chucked": True,
                    "chunk_size": 2,
                    "response": {
                        "user_ids": [1, 2, 3]
                    }
                }
            }
        })

        self.assertEqual(self.app.get('/users').data, b'{"user_ids": [1, 2, 3]}')

    def test_pagination(self):
        config.update({
            "users": {
                "get": {
                }
            }
        })

    def test_invalid_path(self):
        self.assertEqual(self.app.get('/users/invalid').status_code, 404)

    def test_invalid_method(self):
        config.update({
            "users": {
                "get": {
                    "response": {
                        "user_ids": [1, 2, 3]
                    }
                }
            }
        })

        self.assertEqual(self.app.post('/users').status_code, 405)

    def test_abortion(self):
        config.update({
            "users": {
                "get": {
                    "abort": 503
                }
            }
        })

        self.assertEqual(self.app.get('/users').status_code, 503)


class TestInteractiveMode(TestCase):
    def setUp(self):
        self.app = app.test_client()


class TestDummyMode(TestCase):
    def setUp(self):
        self.app = app.test_client()
