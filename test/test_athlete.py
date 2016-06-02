# http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure

# Run python -m unittest test.test_athlete


import unittest, urllib
from strava import athlete, utilities


class TestAthleteConstructor(unittest.TestCase):

    def test_init_with_no_input_arguments(self):
        self.athlete = athlete.Athlete()
        self.failUnless(isinstance(self.athlete.athlete_id, basestring))
        self.failUnless(len(self.athlete.athlete_id) > 0)

    def test_init_with_access_token_input_argument(self):
        self.access_token = 'test_token'
        self.athlete = athlete.Athlete(access_token=self.access_token)
        self.assertEqual(self.athlete.access_token, self.access_token)


class TestAthleteRequestsJSON(unittest.TestCase):

    def setUp(self):
        self.athlete = athlete.Athlete()

    def test_retrieve_current_athlete_should_returnNonEmptyStr(self):
        self.athlete.retrieve_current_athlete_json()
        self.failUnless(len(self.athlete.current_athlete_json) > 0)

    def test_retrieve_list_athlete_activities_json_should_returnStr(self):
        self.athlete.retrieve_list_athlete_activities_json()
        self.failIf(self.athlete.list_of_activities_json == 'StravaEndpointRequestError')
        self.failUnless(isinstance(self.athlete.list_of_activities_json, basestring))

    def test_retrieve_list_athlete_activities_json_after_should_returnStr(self):
        _date_after_str = "1970-01-01T00:00:01Z" # 1 sec from Epoch
        self.athlete.retrieve_list_athlete_activities_json(params=_date_after_str)
        self.failIf(self.athlete.list_of_activities_json == 'StravaEndpointRequestError')
        self.failUnless(isinstance(self.athlete.list_of_activities_json, basestring))
