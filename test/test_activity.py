import unittest
from strava import client, athlete, activity

class TestActivity(unittest.TestCase):

    def setUp(self):
        self.activity_id = '587646088'
        self.client   = client.Client() # not needed for now, but will be required for access_token exchange
        self.athlete  = athlete.Athlete()
        self.activity = activity.Activity(athlete=self.athlete, activity_id=self.activity_id)

    def test_whenCall_activity_json_should_return_NonZeroStr(self):
        self.failUnless(isinstance(self.activity.activity_json, basestring))