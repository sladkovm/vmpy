import unittest, json
import numpy as np
from mock import patch, MagicMock
from strava import athlete, streams, utilities

# Run python -m unittest test.test_streams

class TestStreamsConstrutor(unittest.TestCase):

    mock_activity_id = '321934'
    mock_athlete = MagicMock(name='athlete')
    mock_streams_json = {'time':None,
                             'latlng':None,
                             'distance':None,
                             'altitude':None,
                             'velocity_smooth':None,
                             'heartrate':None,
                             'cadence':None,
                             'watts':None,
                             'temp':None,
                             'moving':None,
                             'grade_smooth':None}
    mock_streams_dict = {'time': None,
                             'latlng': None,
                             'distance': None,
                             'altitude': None,
                             'velocity_smooth': None,
                             'heartrate': None,
                             'cadence': None,
                             'watts': None,
                             'temp': None,
                             'moving': None,
                             'grade_smooth': None}
    mock_streams_dict_np = {'time': None,
                             'latlng': None,
                             'distance': None,
                             'altitude': None,
                             'velocity_smooth': None,
                             'heartrate': None,
                             'cadence': None,
                             'watts': None,
                             'temp': None,
                             'moving': None,
                             'grade_smooth': None}

    @patch('strava.athlete.Athlete', return_value=mock_athlete)
    @patch.object(streams.Streams, '_retrieve_activity_streams',
                  return_value = (mock_streams_json, mock_streams_dict, mock_streams_dict_np))
    def test_call_retrieve_activity_streams(self, mock_retrieve_activity_streams, mock_class_Athlete):
        test_athlete = athlete.Athlete()
        test_streams = streams.Streams(self.mock_activity_id, test_athlete)
        # mock_retrieve_activity_streams.assert_called_once()
        self.assertEqual(test_streams.athlete, self.mock_athlete)
        self.assertEqual(test_streams.streams_json, self.mock_streams_json)
        self.assertEqual(test_streams.streams_dict, self.mock_streams_dict)
        self.assertEqual(test_streams.streams_dict_np, self.mock_streams_dict_np)

if (__name__=='__main__'):
    unittest.main()



