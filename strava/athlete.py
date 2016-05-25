import json, os, logging
logger = logging.getLogger(__name__)

class Athlete:
    def __init__(self):
        self.athlete_id = ''
        self.access_token = ''
        self._init_from_athlete_config()

    def _init_from_athlete_config(self):
        logger.info('Initializing athlete from ./config/athlete.config')
        if 'athlete.config' in os.listdir('./config'):
            _athlete_json = open('./config/athlete.config', 'r').read()
        else:
            raise ImportError('File ./config/athlete.config not found')
        _athlete_dict = json.loads(_athlete_json)
        self.athlete_id = _athlete_dict['athlete_id']
        self.access_token = _athlete_dict['access_token']
        return self

if __name__ == "__main__":
    test_athlete = Athlete()