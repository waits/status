import status
import unittest

class StatusTestCase(unittest.TestCase):

    def setUp(self):
        status.app.config['TESTING'] = True
        self.app = status.app.test_client()

    def test_empty_config(self):
        status.app.config['SITES'] = []
        r = self.app.get('/')
        assert 'No sites have been configured yet.' in str(r.data)

    def test_good_site(self):
        status.app.config['SITES'] = [{'name': 'Test Site', 'url': 'http://httpbin.org', 'status': 'OK', 'last_checked': 1458245339}]
        r = self.app.get('/')
        assert 'All systems operational.' in str(r.data)

    def test_bad_site(self):
        status.app.config['SITES'] = [{'name': 'Test Site', 'url': 'http://httpbin.org/status/404', 'status': 404, 'last_checked': 1458245339}]
        r = self.app.get('/')
        assert 'Systems are down!' in str(r.data)

    def test_mixed_status(self):
        status.app.config['SITES'] = [{'name': 'Test Site', 'status': 200, 'last_checked': 1458245339}, {'name': 'Test Site', 'status': 404, 'last_checked': 1458245339}]
        r = self.app.get('/')
        assert 'Systems are down!' in str(r.data)

if __name__ == '__main__':
    unittest.main()
