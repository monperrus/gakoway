
import unittest
import json
from gateway import app

class GatewayTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_hello(self):
        # We assume integration_tests/basic_test.py exists
        # content: def hello(): return 'world'
        rv = self.app.get('/integration_tests/basic_test/hello')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.get_json(), 'world')

    def test_module_doc(self):
        rv = self.app.get('/integration_tests/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Integration Tests Module", rv.get_json())

    def test_arg_passing_add(self):
        rv = self.app.post('/arg_test/funcs/add', 
                           data=json.dumps({'a': 10, 'b': 32}),
                           content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.get_json(), 42)

    def test_arg_passing_legacy(self):
        rv = self.app.post('/arg_test/funcs/echo_request', 
                           data=json.dumps({'msg': 'hello'}),
                           content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.get_json(), 'hello')

    def test_arg_passing_mixed(self):
        rv = self.app.post('/arg_test/funcs/mixed', 
                           data=json.dumps({'a': 'Title:', 'b': 'Content'}),
                           content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.get_json(), 'Title: Content')

if __name__ == '__main__':
    unittest.main()
