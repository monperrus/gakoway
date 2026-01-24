
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

    def test_syspath_import(self):
        # syspath_test/main.py imports 'helper' which is in the same folder.
        # This requires syspath_test to be in sys.path
        rv = self.app.get('/syspath_test/main/run')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.get_json(), 'helped')

if __name__ == '__main__':
    unittest.main()
