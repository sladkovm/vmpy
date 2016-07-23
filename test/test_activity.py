import unittest, json
from mock import patch, MagicMock
from strava import client, athlete, activity

class TestActivityInit(unittest.TestCase):

    mock_athlete = '{}'
    mock_athlete_id = 227615
    mock_activity_id = '321934'
    mock_activity_summary_json = '{}'
    mock_activity_summary_dict = json.loads(mock_activity_summary_json)
    mock_activity_streams = 'mock_stream_object'

    @patch.object(activity.Activity, '_retrieve_activity_streams', return_value=mock_activity_streams)
    @patch.object(activity.Activity, '_retrieve_activity_summary',
                  return_value=(mock_activity_summary_json, mock_activity_summary_dict))
    @patch.object(activity.Activity, '_init_athlete', return_value = mock_athlete)
    def test_init_athlete_is_called(self,
                                    mock_init_athlete, mock_retrieve_activity_summary, mock_retrieve_activity_streams):
        test_activity = activity.Activity(self.mock_activity_id)
        mock_init_athlete.assert_called_with(None)
        self.assertEqual(test_activity.athlete, self.mock_athlete)

    @patch.object(activity.Activity, '_retrieve_activity_streams', return_value=mock_activity_streams)
    @patch.object(activity.Activity, '_retrieve_activity_summary',
                  return_value=(mock_activity_summary_json, mock_activity_summary_dict))
    @patch('strava.athlete.Athlete', return_value = mock_athlete)
    def test_athlet_instantiation_if_no_athlete_provided(self,
                                                         mock_class_Athlete, mock_retrieve_activity_summary, mock_retrieve_activity_streams):
        test_activity = activity.Activity(self.mock_activity_id)
        # mock_class_Athlete.assert_called()
        self.assertEqual(test_activity.athlete, self.mock_athlete)

    @patch.object(activity.Activity, '_retrieve_activity_streams', return_value=mock_activity_streams)
    @patch.object(activity.Activity, '_retrieve_activity_summary',
                  return_value=(mock_activity_summary_json, mock_activity_summary_dict))
    @patch('strava.athlete.Athlete', return_value=mock_athlete)
    def test_athlete_is_passed_through_when_provided(self,
                                                     mock_class_Athlete, mock_retrieve_activity_summary, mock_retrieve_activity_streams):
        test_athlete = athlete.Athlete()
        test_activity = activity.Activity(self.mock_activity_id, _athlete=test_athlete)
        # mock_class_Athlete.assert_called_once()
        self.assertEqual(test_activity.athlete, self.mock_athlete)

    @patch.object(activity.Activity, '_retrieve_activity_streams', return_value=mock_activity_streams)
    @patch.object(activity.Activity, '_retrieve_activity_summary',
                  return_value=(mock_activity_summary_json, mock_activity_summary_dict))
    @patch('strava.athlete.Athlete', return_value=mock_athlete)
    def test_call_retrieve_current_activity_summary(self,
                                                    mock_class_Athlete, mock_retrieve_activity_summary, mock_retrieve_activity_streams):
        test_activity = activity.Activity(self.mock_activity_id)
        # mock_retrieve_activity_summary.assert_called_once()
        self.assertEqual(test_activity.activity_json, self.mock_activity_summary_json)
        self.assertEqual(test_activity.activity_dict, self.mock_activity_summary_dict)

    @patch.object(activity.Activity, '_retrieve_activity_streams', return_value=mock_activity_streams)
    @patch.object(activity.Activity, '_retrieve_activity_summary',
                  return_value=(mock_activity_summary_json, mock_activity_summary_dict))
    @patch('strava.athlete.Athlete', return_value=mock_athlete)
    def test_call_retrieve_activity_streams(self,
                                            mock_class_Athlete, mock_retrieve_activity_summary, mock_retrieve_activity_streams):
        test_activity = activity.Activity(self.mock_activity_id)
        # mock_retrieve_activity_streams.assert_called_once()
        self.assertEqual(test_activity.streams, self.mock_activity_streams)


if (__name__=='__main__'):
    unittest.main()



#
# class TestActivityMetricsInit(unittest.TestCase):
#
#     def SetUp(self):
#         self.activity_id = '628508858' #mdd30
#         self.client   = client.Client() # not needed for now, but will be required for access_token exchange
#         self.athlete  = athlete.Athlete()
#         self.activity = activity.Activity(athlete=self.athlete, activity_id=self.activity_id)
#
#     # def test_init_activity_metrics_should_return_correct_class(self):
#     #     self.activity_metrics = activity.ActivityMetrics(athlete=self.athlete, activity=self.activity)
#     #     # Assert correct class init
#     #     self.assertEqual(str(self.activity_metrics.__class__), 'strava.activity.ActivityMetrics')