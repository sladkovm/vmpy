import logging
import numpy as np
import utilities, athlete

logger = logging.getLogger(__name__)

class Streams():
    '''
    Info: https://strava.github.io/api/v3/streams/#activity

    #ToDo: Retrieve JSON streams and store them as a JSON object
    '''
    TYPES = ['time', 'latlng', 'distance', 'altitude', 'velocity_smooth',
             'heartrate', 'cadence', 'watts', 'temp', 'moving', 'grade_smooth']

    DICT_SCHEMA = {'time':None,
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

    def __init__(self, activity_id, athlete=None):
        self.activity_id = activity_id
        self.streams_json = self.DICT_SCHEMA
        self.streams_dict = self.DICT_SCHEMA
        self.streams_dict_np = self.DICT_SCHEMA
        self.athlete = self._init_athlete(athlete)
        (self.streams_json,
         self.streams_dict,
         self.streams_dict_np) = self._retrieve_activity_streams()

    def _init_athlete(self, _athlete):
        if (_athlete==None):
            _athlete = athlete.Athlete()
        return _athlete

    def _retrieve_activity_streams(self, types=None):
        '''
        Will retrive all available activity streams and populate the JSON dict attribute with the results
        '''
        _access_token = self.athlete.access_token
        logger.info('Retreiving Streams for activity with ID = %s', self.activity_id)
        URL_BASE = 'https://www.strava.com/api/v3/activities/'
        if (types==None):
            types=Streams.TYPES
        if (isinstance(types, basestring)): # when only one type is provided, the compiler treats it as a string iso list
            tmp = types
            types = []
            types.append(tmp)
        _response_json = {}
        _response_dict  = {}
        _response_dict_np = {}
        for stream_type in types:
            _url = URL_BASE + self.activity_id +'/streams/'+ stream_type
            _response_json[stream_type]  = utilities.Utilities.strava_endpoint_request(url=_url, access_token=_access_token)
            _response_dict[stream_type] = utilities.Utilities.json_to_dict(_response_json[stream_type])
            _np_array = self._extract_np_array_from_dict(_response_dict[stream_type], stream_type)
            _response_dict_np[stream_type]   = _np_array
        # logger.debug('Response is %s', _response)
        return (_response_json, _response_dict, _response_dict_np)

    def _extract_np_array_from_dict(self, dict_stream, stream_type):
        '''
        TODO: add validation of the extracted parameters
        '''

        if (stream_type in ['altitude', 'cadence', 'grade_smooth', 'heartrate', 'moving', 'temp', 'velocity_smooth', 'watts']):
            _data = dict_stream[1]['data']
        elif (stream_type in ['distance', 'time', 'latlng']):
            _data = dict_stream[0]['data']
        else:
            raise LookupError
        if (stream_type in ['moving']):
            _np_stream = np.asarray(_data, dtype=bool)
        else:
            _np_stream = np.asarray(_data, dtype=float)
        return _np_stream


if (__name__=='__main__'):
    test_activity_id = '587646088'
    test_athlete = athlete.Athlete()
    test_streams = Streams(test_activity_id)

    print