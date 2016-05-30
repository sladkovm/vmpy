import logging, json, urllib2
logger = logging.getLogger(__name__)

class Activity():
    '''
    Activities are the base object for Strava runs, rides, swims etc.

    Req #1: Returns a detailed representation (JSON) if the activity is owned by the requesting athlete and stores it
            in the activity_json attribute
    '''
    def __init__(self, athlete, activity_id):
        self.activity_id = activity_id
        self.athlete = athlete
        self.activity_json = None
        self.activity_dict = None
        self._retrieve_an_activity()
        self._json_to_dict()

    def _retrieve_an_activity(self, include_all_efforts=None):
        ''' https://strava.github.io/api/v3/athlete/'''
        logger.info('Retrieving an activity with id = %s', self.activity_id)
        _url = 'https://www.strava.com/api/v3/activities/' + self.activity_id
        _req = urllib2.Request(_url)
        _req.add_header("Authorization", "Bearer " + self.athlete.access_token)
        _response = urllib2.urlopen(_req).read()
        logger.debug('Retrieving current activity response: %s', _response)
        self.activity_json = _response

    def _json_to_dict(self):
        logger.info('Converting JSON to dict')
        self.activity_dict = json.loads(self.activity_json)


