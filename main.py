import os, json, logging
from strava import athlete, client

# Set up logging
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # logger.info('Started')
    test_client = client.Client()
    test_athlete = athlete.Athlete()
    test_client.retrieve_current_athlete_json(test_athlete)
