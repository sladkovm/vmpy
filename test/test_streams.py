import unittest, urllib2
from strava import athlete, streams, utilities

class TestStreamsConstrutor(unittest.TestCase):

    def setUp(self):
        self.athlete = athlete.Athlete()
        self.activity_id = '587646088'

    def test_init_streams_with_activity_id(self):
        self.streams = streams.Streams(activity_id=self.activity_id)
        self.assertEqual(str(self.streams.__class__), 'strava.streams.Streams')
        self.assertEqual(self.streams.time, None)
        self.assertEqual(self.streams.latlng, None)
        self.assertEqual(self.streams.distance, None)
        self.assertEqual(self.streams.altitude, None)
        self.assertEqual(self.streams.velocity_smooth, None)
        self.assertEqual(self.streams.heartrate, None)
        self.assertEqual(self.streams.cadence, None)
        self.assertEqual(self.streams.watts, None)
        self.assertEqual(self.streams.temp, None)
        self.assertEqual(self.streams.moving, None)
        self.assertEqual(self.streams.grade_smooth, None)

class TestRetrieveStreams(unittest.TestCase):

    def setUp(self):
        self.athlete = athlete.Athlete()
        self.activity_id = '587646088'
        self.streams = streams.Streams(activity_id=self.activity_id)

    def test_call_retrieve_activity_streams_one_type_should_return_NonZeroStr(self):
        for stream_type in self.streams.TYPES:
            self.response = self.streams.retrieve_activity_streams(access_token=self.athlete.access_token,
                                                                   types=stream_type)
            self.assertIsInstance(self.response, dict)
            self.failIf(self.response[stream_type]=='StravaEndpointRequestError')

    def test_call_retrieve_activity_streams_all_types_should_return_NonZeroStr(self):
        self.response = self.streams.retrieve_activity_streams(access_token=self.athlete.access_token,
                                                               types=self.streams.TYPES)
        self.assertIsInstance(self.response, dict)
        self.failIf(self.response=='StravaEndpointRequestError')


