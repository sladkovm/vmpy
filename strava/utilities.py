import dateutil.parser, urllib2, json
import logging
logger = logging.getLogger(__name__)

class Utilities():
    '''
    Class Utilities provides a set of static methods to be used across all application.
    Ex.: Utilities.strava_endpoint_request()
    '''

    @staticmethod
    def seconds_since_epoch(time_ISO8601_str):
        '''
        Utility to convert ISO8601 str into {int} seconds_since_epoch
        :param time_ISO8601_str:
        :return: {int} seconds_since_epoch
        '''
        _EPOCH = dateutil.parser.parse("1970-01-01T00:00:00Z")
        _time_datetime_object = dateutil.parser.parse(time_ISO8601_str)
        _delta_wrt_epoch = _time_datetime_object - _EPOCH
        _delta_sec = int(_delta_wrt_epoch.total_seconds())
        return _delta_sec

    @staticmethod
    def strava_endpoint_request(url, access_token, data = None):
        '''
        Wrapper around Strava RESTful API
        :param url: Example 'https://www.strava.com/api/v3/athlete/activities'
        :param access_token: usualy must be found in the instance of athlete.Athlete()
        :param data: urllib.urlencode({key: value})
        :return: {str} response
        '''
        _url = url
        _headers = {"Authorization": "Bearer " + access_token}
        _data = data # already encoded using the urllib.urlencode

        if (_data==None):
            _req = urllib2.Request(url=_url, headers=_headers)
        else:
            _req = urllib2.Request(url = _url + '?' + _data, headers=_headers)
        logger.debug('Request = %s', _req)
        _response = urllib2.urlopen(_req)
        if (_response.code==200):
            _response_read = _response.read()
        else:
            # logger.error('Strava Endpoint request %s returned code %i', _req, _response.code)
            _response_read = 'StravaEndpointRequestError'
        return _response_read

    @staticmethod
    def json_to_dict(JSON_in):
        logger.info('Converting JSON activity to dict')
        dict_out = json.loads(JSON_in)
        return dict_out