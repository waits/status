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
        status.app.config['SITES'] = [{'name': 'Test Site', 'url': 'http://httpbin.org'}]
        r = self.app.get('/')
        assert 'All systems operational.' in str(r.data)

    def test_bad_site(self):
        status.app.config['SITES'] = [{'name': 'Test Site', 'url': 'http://httpbin.org/status/404'}]
        r = self.app.get('/')
        assert 'Systems are down!' in str(r.data)

if __name__ == '__main__':
    unittest.main()
