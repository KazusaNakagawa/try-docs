import unittest
import requests
import requests_mock


class TestRequest(unittest.TestCase):

    def __init__(self, methodName) -> None:
        super().__init__(methodName=methodName)
        self.test_url = 'http://example.com/test'

    def test_reqest(self):
        session = requests.Session()
        adapter = requests_mock.Adapter()
        session.mount('mock://', adapter)

        adapter.register_uri('GET', 'mock://test.com', text='data')
        resp = session.get('mock://test.com')

        self.assertEqual(resp.status_code, 200, 'レスポンスが 200 であること')
        self.assertEqual(resp.text, 'data', 'テキストが data であること')

    def test_request_get(self):
        with requests_mock.Mocker() as m:
            m.get(self.test_url, text='data')
            r = requests.get(self.test_url).text
        self.assertEqual(r, 'data', 'テキストが data であること')

    def test_403_error(self):
        with requests_mock.Mocker() as m:
            m.get(self.test_url, status_code=403, text='Forbidden')
            response = requests.get(self.test_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.text, 'Forbidden')


if __name__ == '__main__':
    unittest.main()
