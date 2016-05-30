import json, os, logging, urllib, urllib2, dateutil.parser
logger = logging.getLogger(__name__)

class Athlete:
    '''
    Athletes are Strava users, Strava users are athletes.
    The object is returned in detailed, summary or meta representations.

    https://strava.github.io/api/v3/athlete/

    >>> from strava import athlete

    Req #1 Init athlete object using the explicit access_token (providing athlete_id is optional)
           or based on the "config/athlete.config" file
    >>> test_athlete = athlete.Athlete()

    Req #2 Retrieve information about the currently authenticated athlete (access_token is known).
           Returns a detailed representation of the athlete.

    >>> test_athlete.retrieve_current_athlete_json()
    >>> len(test_athlete.current_athlete_json) > 0
    True

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
        if 'athlete.config' in os.listdir('./config'):
            _athlete_json = open('./config/athlete.config', 'r').read()
        else:
            raise ImportError('File ./config/athlete.config not found')
        _athlete_dict = json.loads(_athlete_json)
        self.athlete_id = _athlete_dict['athlete_id']
        self.access_token = _athlete_dict['access_token']

    def retrieve_current_athlete_json(self):
        logger.info('Retrieving current athlete')
        _url = 'https://www.strava.com/api/v3/athlete'
        _response = self._strava_endpoint_request(_url)
        logger.debug('Retrieving current athlete response: %s', _response)
        self.current_athlete_json = _response

    def retrieve_list_athlete_activities_json(self, params=None):
        logger.info('Retrieving list of activities with params=%s', params)
        _url = 'https://www.strava.com/api/v3/athlete/activities'
        if (params==None):
            _response = self._strava_endpoint_request(_url)
        else:
            _response = self._strava_endpoint_request(url=_url, data=params)
        self.list_of_activities_json = _response
        logger.debug('Retrieving list_of_activities: %s', self.list_of_activities_json)

    def _strava_endpoint_request(self, url, data = None):
        '''
        :param url: Example 'https://www.strava.com/api/v3/athlete/activities'
        :param data: urllib.urlencode({key: value})
        :return: {str}
        '''
        _url = url
        _data = data # already encoded using the urllib.urlencode
        _headers = {"Authorization" : "Bearer " + self.access_token}
        if (_data==None):
            _req = urllib2.Request(url=_url, headers=_headers)
        else:
            _req = urllib2.Request(url = _url + '?' + _data, headers=_headers)
        logger.debug('Request = %s', _req)
        _response = urllib2.urlopen(_req)
        if (_response.code==200):
            _response_read = _response.read()
        else:
            logger.error('Strava Endpoint request %s returned code %i', _req, _response.code)
            _response_read = 'StravaEndpointRequestError'
        return _response_read

    def _seconds_since_epoch(self, time_ISO8601_str):
        _EPOCH = dateutil.parser.parse("1970-01-01T00:00:00Z")
        _time_datetime_object = dateutil.parser.parse(time_ISO8601_str)
        _delta_wrt_epoch = _time_datetime_object - _EPOCH
        _delta_sec = int(_delta_wrt_epoch.total_seconds())
        return _delta_sec


if __name__ == "__main__":
    test_athlete = Athlete()