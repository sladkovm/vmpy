import os, json, logging
import dateutil.parser, datetime
import urllib, urllib2
from strava import athlete, client, activity

# Set up logging
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # logger.info('Started')
    # test_client = client.Client()


    test_athlete = athlete.Athlete()
    test_athlete.retrieve_current_athlete_json()

    test_class = test_athlete.__class__
    test_class_str = str(test_class)
    # print test_athlete.current_athlete_json

    #
    # test_athlete.retrieve_list_athlete_activities_json()
    # print test_athlete.list_of_activities_json
    #

    # test_athlete.retrieve_list_athlete_activities_json(params="2016-05-25T12:48:05Z")
    # print test_athlete.list_of_activities_json


    test_activity_id = '587646088'
    test_activity    = activity.Activity(athlete=test_athlete, activity_id=test_activity_id)
    print test_activity.activity_json

