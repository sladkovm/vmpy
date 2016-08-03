import json, os, imp, logging
import utilities


logger = logging.getLogger(__name__)

class Athlete:
    '''
    Athletes are Strava users, Strava users are athletes.
    The object is returned in detailed, summary or meta representations.
    Info: https://strava.github.io/api/v3/athlete/
    '''

    def __init__(self, access_token='', athlete_id=''):
        # pre-init attributes
        self.athlete_id = None
        self.access_token = None
        self.current_athlete_json = None
        self.current_athlete_dict = None
        self.list_of_activities_json = None
        self.list_of_activities_dict = None
        # ---
        (self.access_token, self.athlete_id) = self._init_current_athlete(access_token, athlete_id)
        self.current_athlete_json = self._retrieve_current_athlete_json(self.access_token)
        self.current_athlete_dict = utilities.Utilities.json_to_dict(self.current_athlete_json)

    # --- Private methods -------
    def _init_current_athlete(self, access_token, athlete_id):
        if (len(access_token)==0): # access_token is not provided
            logger.info('Initializing athlete from ./config/athlete.config')
            (access_token, athlete_id) = self._init_from_athlete_config()
        else: # access_token is explicitely provided
            #TODO: The athlete_id must also be checked for this case
            logger.info('Initializing athlete using provided \n access_token = %s \n athlete_id = %s', self.access_token, self.athlete_id)
            pass
        return (access_token, athlete_id)

    def _init_from_athlete_config(self):
        _athlete_id   = None
        _access_token = None
        append_path = imp.find_module('config')[1]
        if 'athlete.config' in os.listdir(append_path):
            _athlete_json = open(append_path + '/athlete.config', 'r').read()
        else:
            raise ImportError('File ./config/athlete.config not found')
        _athlete_dict = json.loads(_athlete_json)
        _athlete_id   = _athlete_dict['athlete_id']
        _access_token = _athlete_dict['access_token']
        return (_access_token, _athlete_id)

    def _retrieve_current_athlete_json(self, access_token):
        '''
        Info: https://strava.github.io/api/v3/athlete/#get-details
        :return: None
        '''
        logger.info('Retrieving current athlete')
        _url = 'https://www.strava.com/api/v3/athlete'
        _response = utilities.Utilities.strava_endpoint_request(url=_url, access_token=access_token)
        logger.debug('Retrieving current athlete response: %s', _response)
        return _response

    # --- Public methods -------
    # TODO this method must be tested
    def retrieve_list_athlete_activities_json(self, params=None):
        '''
        Info: https://strava.github.io/api/v3/activities/#get-activities
        :param params: urllib.urlencode({after: _seconds_since_epoch})
        :return: None
        '''
        logger.info('Retrieving list of activities with params=%s', params)
        _url = 'https://www.strava.com/api/v3/athlete/activities'
        if (params==None):
            _response = utilities.Utilities.strava_endpoint_request(url=_url, access_token=self.access_token)
        else:
            _response = utilities.Utilities.strava_endpoint_request(url=_url, access_token=self.access_token, data=params)
        self.list_of_activities_json = _response
        self.list_of_activities_dict = utilities.Utilities.json_to_dict(_response)
        logger.debug('Retrieving list_of_activities: %s', self.list_of_activities_json)

    def print_list_athlete_activities(self):
        if (self.list_of_activities_dict==None):
            logger.info('Activity list is not retrived, retrieving the list')
            self.retrieve_list_athlete_activities_json()
        for _activity in self.list_of_activities_dict:
            print '%s \t id:%s \t %s' %(_activity['start_date_local'], _activity['id'], _activity['name'])


if __name__ == "__main__":

    # Init from config
    test_athlete = Athlete()
    print test_athlete

