# http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure

# Run python -m unittest test.test_client

import unittest
from strava import client
from strava import athlete


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = client.Client()
        self.athlete = athlete.Athlete()

    def test_whenCall_attr_client_id_should_returnNonEmptyStr(self):
        self.failUnless(isinstance(self.client.client_id, basestring))
        self.failUnless(len(self.client.client_id) > 0)

    def test_whenCall_attr_client_secret_should_returnNonEmptyStr(self):
        self.failUnless(isinstance(self.client.client_secret, basestring))
        self.failUnless(len(self.client.client_secret) > 0)

    def test_retrieve_current_athlete_should_returnNonEmptyStr(self):
        self.client.retrieve_current_athlete_json(self.athlete)
        self.failUnless(len(self.client.current_athlete_json) > 0)
