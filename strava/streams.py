import logging
from strava import utilities, athlete

logger = logging.getLogger(__name__)

class Streams():
    '''
    Info: https://strava.github.io/api/v3/streams/#activity
    '''
    TYPES = ['time', 'latlng', 'distance', 'altitude', 'velocity_smooth',
             'heartrate', 'cadence', 'watts', 'temp', 'moving', 'grade_smooth']

    def __init__(self, activity_id):
        self.activity_id = activity_id
        self.time = None
        self.latlng = None
        self.distance = None
        self.altitude = None
        self.velocity_smooth = None
        self.heartrate = None
        self.cadence = None
        self.watts = None
        self.temp = None
        self.moving = None
        self.grade_smooth = None

    def retrieve_activity_streams(self, access_token, types=None):
        logger.info('Retreiving Streams for activity with ID = %s', self.activity_id)
        URL_BASE = 'https://www.strava.com/api/v3/activities/'
        if (types==None):
            types=Streams.TYPES
        if (isinstance(types, basestring)): # when only one type is provided, the compiler treats it as a string iso list
            tmp = types
            types = []
            types.append(tmp)
        _response = {}
        for stream_type in types:
            _url = URL_BASE + self.activity_id +'/streams/'+ stream_type
            _response[stream_type] = utilities.Utilities.strava_endpoint_request(url=_url, access_token=access_token)
        # logger.debug('Response is %s', _response)
        return _response


if (__name__=='__main__'):
    test_activity_id = '587646088'
    test_athlete = athlete.Athlete()
    test_streams = Streams(activity_id=test_activity_id)
    test_streams.retrieve_activity_streams(access_token=test_athlete.access_token, types=Streams.TYPES[1])