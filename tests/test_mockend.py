import json
import time
from copy import deepcopy
from unittest import TestCase
from mockend import config, app, validate_path


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
                            "email": "J.Doe@email.com"
                        }
                    }
                }
            }
        })

        response = json.dumps({
            "name": "John Doe",
            "email": "J.Doe@email.com"
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
                    "chunked": True,
                    "chunk_size": 2,
                    "response": {
                        "user_ids": [1, 2, 3]
                    }
                }
            }
        })

        self.assertEqual(self.app.get('/users').data, b'{"user_ids": [1, 2, 3]}')

    def test_interactive_mode_pagination(self):
        config.update({
            "users": {
                "interactive": True,
                "pagination": True,
                "get": {},
                "post": {}
            }
        })

        self.app.post('/users/JohnDoe', data=json.dumps(
            {
                "name": "John Doe",
                "email": "J.Don@email.com"
            }
        ).encode('utf-8'))

        self.app.post('/users/Alice', data=json.dumps(
            {
                "name": "Alice",
                "email": "alice@email.com"
            }
        ).encode('utf-8'))

        self.app.post('/users/Bob', data=json.dumps(
            {
                "name": "Bob",
                "email": "bob@email.com"
            }
        ).encode('utf-8'))

        print(self.app.get('/users?start=Alice&limit=2').data)

        self.assertEqual(self.app.get('/users?start=Alice&limit=2').data, json.dumps(
            {
                "Alice":
                    {
                        "name": "Alice",
                        "email": "alice@email.com"
                    },
                "Bob": {
                    "name": "Bob",
                    "email": "bob@email.com"}
            }).encode('utf-8'))

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

    def test_dummy_mode(self):
        config.update({
            "users": {
                "post": {
                    "dummy": True
                }
            }
        })

        request_body = json.dumps({
            "user_ids": [1, 2, 3]
        }).encode('utf-8')

        self.assertEqual(self.app.post('/users', data=request_body).data, request_body)

    def test_interactive_invalid_path(self):
        config.update({
            "users": {
                "interactive": True,
                "get": {},
                "post": {}
            }
        })

        self.assertEqual(self.app.get('/users/invalid').status_code, 404)

    def test_interactive_insert(self):
        config.update({
            "users": {
                "interactive": True,
                "get": {},
                "post": {}
            }
        })

        self.app.post('/users/JohnDoe', data=json.dumps(
            {
                "name": "John Doe",
                "email": "J.Don@email.com"
            }
        ).encode('utf-8'))

        self.assertEqual(self.app.get('/users').data, json.dumps(
            {
                "JohnDoe": {
                    "name": "John Doe",
                    "email": "J.Don@email.com"
                }
            }
        ).encode('utf-8'))

        self.assertEqual(self.app.get('/users/JohnDoe').data, json.dumps(
            {

                "name": "John Doe",
                "email": "J.Don@email.com"

            }
        ).encode('utf-8'))

    def test_interactive_update(self):
        config.update({
            "users": {
                "interactive": True,
                "get": {},
                "post": {},
                "put": {},
            }
        })

        self.app.post('/users/JohnDoe', data=json.dumps(
            {
                "name": "John Doe",
                "email": "J.Don@email.com"
            }
        ).encode('utf-8'))

        self.app.put('/users/JohnDoe', data=json.dumps(
            {
                "name": "John Doe",
                "email": "J.Don@gmail.com"
            }
        ).encode('utf-8'))

        self.assertEqual(self.app.get('/users/JohnDoe').data, json.dumps(
            {

                "name": "John Doe",
                "email": "J.Don@gmail.com"

            }
        ).encode('utf-8'))

    def test_interactive_delete(self):
        config.update({
            "users": {
                "interactive": True,
                "get": {},
                "post": {},
                "delete": {},
            }
        })

        self.app.post('/users/JohnDoe', data=json.dumps(
            {
                "name": "John Doe",
                "email": "J.Don@email.com"
            }
        ).encode('utf-8'))

        self.app.delete('/users/JohnDoe')

        response = json.loads(self.app.get('/users').data)

        self.assertNotIn("JohnDoe", response)


class TestPathValidator(TestCase):
    def test_simple_path_validation(self):
        path = "/users/"
        configuration = {
            "users": {
                "get": {}
            }
        }
        paths, path_config, identifier = validate_path(path, configuration)
        self.assertEqual(paths, ["users"])
        self.assertEqual(path_config, configuration["users"])
        self.assertEqual(identifier, None)

    def test_nested_path_validation(self):
        path = "/users/JohnDoe/posts/"
        configuration = {
            "users": {
                "JohnDoe": {
                    "posts": {
                        "get": {}
                    }
                }
            }
        }

        paths, path_config, identifier = validate_path(path, configuration)
        self.assertEqual(paths, ["users", "JohnDoe", "posts"])
        self.assertEqual(path_config, configuration["users"]["JohnDoe"]["posts"])
        self.assertEqual(identifier, None)

    def test_interactive_mode_path_validation(self):
        path = "/users/JohnDoe/"
        configuration = {
            "users": {
                "interactive": True,
            }
        }

        paths, path_config, identifier = validate_path(path, configuration)
        self.assertEqual(paths, ["users", "JohnDoe"])
        self.assertEqual(path_config, configuration["users"])
        self.assertEqual(identifier, "JohnDoe")
