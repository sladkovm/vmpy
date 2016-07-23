import unittest, urllib
from strava import utilities, athlete

class TestUtilities(unittest.TestCase):

    def test_call_seconds_since_epoch_should_returnInt(self):
        _test_date_str = "1970-01-01T00:00:01Z" # 1 sec from Epoch
        _expected_result_sec = int(1.0)
        _test_date_sec_since_epoch = utilities.Utilities.seconds_since_epoch(_test_date_str)
        self.assertIsInstance(_test_date_sec_since_epoch, int)
        self.assertEqual(_test_date_sec_since_epoch, _expected_result_sec)

    # def test_strava_end_point_request_with_no_data(self):
    #     # This test will be executed against retrieving current athlete request
    #     _test_url = 'https://www.strava.com/api/v3/athlete'
    #     self.response = utilities.Utilities.strava_endpoint_request(url=_test_url, access_token=self.athlete.access_token)
    #     self.failIf(self.response=='StravaEndpointRequestError')
    #     self.failUnless(isinstance(self.response, basestring))
    #     self.failUnless(len(self.response) > 0)

    # def test_strava_end_point_request_with_data_should_returnStr(self):
    #     # This test will be executed against retrieving list of activities after specified date
    #     _test_url = 'https://www.strava.com/api/v3/athlete/activities'
    #     _test_date_after_str = "1970-01-01T00:00:01Z" # 1 sec from Epoch
    #     _seconds_after_since_epoch = utilities.Utilities.seconds_since_epoch(time_ISO8601_str=_test_date_after_str)
    #     _data_values = {'after' : _seconds_after_since_epoch}
    #     _data = urllib.urlencode(_data_values)
    #     self.athlete._response = utilities.Utilities.strava_endpoint_request(url=_test_url, access_token=self.athlete.access_token, data=_data)
    #     self.failIf(self.athlete._response == 'StravaEndpointRequestError')
    #     self.failUnless(isinstance(self.athlete._response, basestring))
    #     self.failUnless(len(self.athlete._response) > 0)

if (__name__=='__main__'):
    unittest.main()