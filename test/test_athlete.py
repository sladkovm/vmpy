# http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure

# Run python -m unittest test.test_athlete


import unittest, json
from mock import patch, MagicMock
from strava import athlete, utilities


class TestAthleteConstructorWithNoInput(unittest.TestCase):

    mock_athlete_id    = 227615
    mock_access_token = "83ebeabdec09f6670863766f792ead24d61fe3f9"
    mock_url = 'https://www.strava.com/api/v3/athlete'
    mock_athlete_json = '{}'
    mock_athlete_dict = json.loads(mock_athlete_json)

    @patch.object(athlete.Athlete, '_retrieve_current_athlete_json', return_value = mock_athlete_json)
    @patch.object(athlete.Athlete, '_init_from_athlete_config', return_value = (mock_access_token, mock_athlete_id))
    def test_init_from_athlete_config_is_called(self, mock_init_from_athlete_config, mock_retrieve_current_athlete_json):
        test_athlete = athlete.Athlete()
        # Assertions correct call
        mock_init_from_athlete_config.assert_called_with()

    @patch.object(athlete.Athlete, '_retrieve_current_athlete_json', return_value = mock_athlete_json)
    @patch.object(athlete.Athlete, '_init_current_athlete', return_value = (mock_access_token, mock_athlete_id))
    def test_init_current_athlete_is_called(self, mock_init_current_athlete, mock_retrieve_current_athlete_json):
        test_athlete = athlete.Athlete()
        mock_init_current_athlete.assert_called_with('', '')
        self.assertEqual(test_athlete.access_token, self.mock_access_token)
        self.assertEqual(test_athlete.athlete_id, self.mock_athlete_id)

    @patch.object(athlete.Athlete, '_retrieve_current_athlete_json', return_value = mock_athlete_json)
    @patch.object(athlete.Athlete, '_init_current_athlete', return_value = (mock_access_token, mock_athlete_id))
    def test_retrieve_current_athlete_json_is_called(self, mock_init_current_athlete, mock_retrieve_current_athlete_json):
        test_athlete = athlete.Athlete()
        mock_retrieve_current_athlete_json.assert_called_with(self.mock_access_token)
        self.assertEqual(test_athlete.current_athlete_json, self.mock_athlete_json)

    @patch.object(utilities.Utilities, 'json_to_dict', return_value = mock_athlete_dict)
    @patch.object(athlete.Athlete, '_retrieve_current_athlete_json', return_value = mock_athlete_json)
    @patch.object(athlete.Athlete, '_init_current_athlete', return_value = (mock_access_token, mock_athlete_id))
    def test_json_to_dict_is_called(self,mock_init_current_athlete,
                                         mock_retrieve_current_athlete_json,
                                         mock_json_to_dict):
        test_athlete = athlete.Athlete()
        mock_json_to_dict.assert_called_with(self.mock_athlete_json)
        self.assertEqual(test_athlete.current_athlete_dict, self.mock_athlete_dict)


class TestAthleteConstructorWithAccessToken(unittest.TestCase):

    def test(self):
        pass

if __name__ == '__main__':
    unittest.main()