import json, os, urllib2, logging
import athlete

logger = logging.getLogger(__name__)

class Client:
    """
    This class implements an application client (a.k.a. client) to the Strava API.

    The object of this class is only necessary to execute an authentification process in order to receive an athlete
    access token that will allow retreiving of the detailed activity information and streams

    https://strava.github.io/api/v3/oauth/

    Requirements:
    Req #1. Client class will instantiate an object with attribute "client_id" and "client_secret" that are non-zero strings
    Req #2.

    Tests:
    """

    def __init__(self):
        self.client_id = ''
        self.client_secret = ''
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


if __name__ == "__main__":
    test_client = Client()