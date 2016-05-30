# http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure

# Run python -m unittest test.test_athlete


import unittest, urllib
from strava import athlete


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


class TestAthleteStravaEndpointRequest(unittest.TestCase):

    def setUp(self):
        self.athlete = athlete.Athlete()

    def test_strava_end_point_request_with_no_data_should_returnStr(self):
        # This test will be executed against retrieving current athlete request
        _test_url = 'https://www.strava.com/api/v3/athlete'
        self.athlete._response = self.athlete._strava_endpoint_request(url=_test_url)
        self.failIf(self.athlete._response=='StravaEndpointRequestError')
        self.failUnless(isinstance(self.athlete._response, basestring))
        self.failUnless(len(self.athlete._response) > 0)

    def test_strava_end_point_request_with_data_should_returnStr(self):
        # This test will be executed against retrieving list of activities after specified date
        _test_url = 'https://www.strava.com/api/v3/athlete/activities'
        _test_date_after_str = "1970-01-01T00:00:01Z" # 1 sec from Epoch
        _seconds_after_since_epoch = self.athlete._seconds_since_epoch(time_ISO8601_str=_test_date_after_str)
        _data_values = {'after' : _seconds_after_since_epoch}
        _data = urllib.urlencode(_data_values)
        self.athlete._response = self.athlete._strava_endpoint_request(url=_test_url, data=_data)
        self.failIf(self.athlete._response == 'StravaEndpointRequestError')
        self.failUnless(isinstance(self.athlete._response, basestring))
        self.failUnless(len(self.athlete._response) > 0)


class TestAthleteUtils(unittest.TestCase):

    def setUp(self):
        self.athlete = athlete.Athlete()

    def test_call_seconds_since_epoch_should_returnInt(self):
        _test_date_str = "1970-01-01T00:00:01Z" # 1 sec from Epoch
        _expected_result_sec = int(1.0)
        _test_date_sec_since_epoch = self.athlete._seconds_since_epoch(_test_date_str)
        self.assertIsInstance(_test_date_sec_since_epoch, int)
        self.assertEqual(_test_date_sec_since_epoch, _expected_result_sec)