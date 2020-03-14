import unittest
from mock import patch, Mock
from mysite.miniapm import MiniAPMMiddleware

class TestMiddleware(unittest.TestCase):
    @patch('mysite.miniapm.MiniAPMMiddleware')
    def test_init(self, my_middleware_mock):
        my_miniapm = MiniAPMMiddleware('response')
        print ("hello")
        assert(my_miniapm.get_response) == 'response'

    def test_miniapmmiddleware(self):
        request = Mock()
        print ("request set")
        my_miniapm = MiniAPMMiddleware(Mock())
        print ("my_miniapm set")
        my_miniapm(request)
        print ("goodbye")
        assert response.content != NULL
