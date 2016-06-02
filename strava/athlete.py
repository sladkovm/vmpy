import json, os, logging, urllib, urllib2, dateutil.parser
from strava import utilities
logger = logging.getLogger(__name__)

class Athlete:
    '''
    Athletes are Strava users, Strava users are athletes.
    The object is returned in detailed, summary or meta representations.
    Info: https://strava.github.io/api/v3/athlete/
    '''

    def __init__(self, access_token='', athlete_id=''):
        self.athlete_id              = athlete_id
        self.access_token            = access_token
        self.current_athlete_json    = None
        self.list_of_activities_json = None
        if (len(self.access_token)==0):
            logger.info('Initializing athlete from ./config/athlete.config')
            self._init_from_athlete_config()
        # if (len(self.athlete_id)==0):

    def _init_from_athlete_config(self):
        if 'athlete.py' in os.listdir('.'): # Class is called from the strava folder
            append_path = '../'
        else: # Class is called from the Root
            append_path = './'
        if 'athlete.config' in os.listdir(append_path + 'config'):
            _athlete_json = open(append_path + 'config/athlete.config', 'r').read()
        else:
            raise ImportError('File ./config/athlete.config not found')
        _athlete_dict = json.loads(_athlete_json)
        self.athlete_id = _athlete_dict['athlete_id']
        self.access_token = _athlete_dict['access_token']

    def retrieve_current_athlete_json(self):
        '''
        Info: https://strava.github.io/api/v3/athlete/#get-details
        :return: None
        '''
        logger.info('Retrieving current athlete')
        _url = 'https://www.strava.com/api/v3/athlete'
        _response = utilities.Utilities.strava_endpoint_request(url=_url, access_token=self.access_token)
        logger.debug('Retrieving current athlete response: %s', _response)
        self.current_athlete_json = _response

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
        logger.debug('Retrieving list_of_activities: %s', self.list_of_activities_json)


if __name__ == "__main__":
    test_athlete = Athlete()