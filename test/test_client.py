# http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure

# Run python -m unittest test.test_client

import unittest
from strava import client
from strava import athlete


class TestClient(unittest.TestCase):

    def test(self):
        pass


if (__name__=='__main__'):
    unittest.main()


