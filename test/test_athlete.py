# http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure

# Run python -m unittest test.test_athlete


import unittest
from strava import athlete

class TestAthlete(unittest.TestCase):

    def setUp(self):
        self.athlete = athlete.Athlete()

    def test_whenCall_attr_athlete_id_should_returnNonEmptyStr(self):
        self.failUnless(isinstance(self.athlete.athlete_id, basestring))
        self.failUnless(len(self.athlete.athlete_id) > 0)

    def test_whenCall_attr_access_token_should_returnNonEmptyStr(self):
        self.failUnless(isinstance(self.athlete.access_token, basestring))
        self.failUnless(len(self.athlete.access_token) > 0)

