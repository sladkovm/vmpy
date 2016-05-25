import json, os, urllib2, logging
import athlete

logger = logging.getLogger(__name__)

class Client:
    """
    This class implements an application client (a.k.a. client) to the Strava API. The strava credentials are read from
    the './config/client.config' file and represented there as a JSON object with "client_id" and "client_secret"
    attributes.

    Requirements:
    Req #1. Client class will instantiate an object with attribute "client_id" and "client_secret" that are non-zero strings
    Req #2. Client object must be able to open connection session to Strava API on behalf of the athlete object and retrieve
            athlete's JSON profile
    Req #3.

    Tested library:
    >>> from strava import client

    Tests:
    """

    def __init__(self):
        self.client_id = ''
        self.client_secret = ''
        self.current_athlete_json = None
        self._init_from_client_config()

    def _init_from_client_config(self):
        logger.info('Initializing client from ./config/client.config')
        if 'client.config' in os.listdir('./config'):
            _client_json = open('./config/client.config', 'r').read()
        else:
            raise ImportError('File ./config/client.config not found')
        _client_dict = json.loads(_client_json)
        self.client_id = _client_dict['client_id']
        self.client_secret = _client_dict['client_secret']
        return self

    def retrieve_current_athlete_json(self, athlete):
        logger.info('Retrieving current athlete')
        ''' https://strava.github.io/api/v3/athlete/'''
        _url = 'https://www.strava.com/api/v3/athlete'
        _req = urllib2.Request(_url)
        _req.add_header("Authorization", "Bearer " + athlete.access_token)
        _response = urllib2.urlopen(_req).read()
        logger.debug('Retrieving current athlete response: %s', _response)
        self.current_athlete_json = _response


if __name__ == "__main__":
    test_client = Client()
    test_athlete = athlete.Athlete()
    test_client.retrieve_current_athlete_json(test_athlete)