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
        status.app.config['SITES'] = [{'name': 'Test Site', 'url': 'http://httpbin.org', 'status': ('ok', 'All good'), 'last_checked': 1458245339}]
        r = self.app.get('/')
        assert 'All systems operational.' in str(r.data)

    def test_bad_site(self):
        status.app.config['SITES'] = [{'name': 'Test Site', 'url': 'http://httpbin.org/status/404', 'status': ('error', 'Reachable but returning errors'), 'last_checked': 1458245339}]
        r = self.app.get('/')
        assert 'Systems are down!' in str(r.data)

    def test_mixed_site(self):
        status.app.config['SITES'] = [{'name': 'Test Site', 'url': 'http://httpbin.org/status/404', 'status': ('caution', 'Slow response'), 'last_checked': 1458245339}]
        r = self.app.get('/')
        assert 'Some services may be degraded or unavailable.' in str(r.data)

    def test_mixed_status(self):
        status.app.config['SITES'] = [{'name': 'Test Site', 'status': ('ok', 'All good'), 'last_checked': 1458245339}, {'name': 'Test Site', 'status': ('error', 'Timeout'), 'last_checked': 1458245339}]
        r = self.app.get('/')
        assert 'Systems are down!' in str(r.data)

if __name__ == '__main__':
    unittest.main()
