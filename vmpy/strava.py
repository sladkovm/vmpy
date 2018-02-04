"""Very thin wrapper around the Strava API v3

    STRAVA_ACCESS_TOKEN must be explicitly provided as an input

    ALL returned values are python objects e.g. dict or list

    Author: Maksym Sladkov
"""
import requests
import json
import logging

logger = logging.getLogger(__name__)


def retrieve_athlete(access_token):
    """Retrieve current(authenticated) athlete
    API V3: https://strava.github.io/api/v3/athlete/#get-details

    :param access_token: Settings/My API Applications/Your Access Token -> str
    :return athlete: -> dict
    """

    endpoint_url = "https://www.strava.com/api/v3/athlete"

    r = requests.get(endpoint_url,
                     headers=authorization_header(access_token))

    if r.ok:

        athlete = json.loads(r.text)

    else:

        logger.error('Retrieve Athlete Failed with a reason {}'.format(r.reason))
        athlete = None

    return athlete


def retrieve_zones(access_token, **kwargs):
    """Retrieve Power and Heartrate zones
    API V3: https://strava.github.io/api/v3/athlete/#zones

    :param access_token: Settings/My API Applications/Your Access Token -> str
    :return zones: -> dict
    """

    endpoint_url = "https://www.strava.com/api/v3/athlete/zones"

    r = requests.get(endpoint_url,
                     headers=authorization_header(access_token))

    if r.ok:

        zones = json.loads(r.text)

    else:

        logger.error('Retrieve Zones Failed with a reason {}'.format(r.reason))
        zones = None

    return zones


def retrieve_activity(activity_id, access_token):
    """Retrieve a detailed representation of activity
    API V3: https://strava.github.io/api/v3/activities/#get-details

    :param activity_id: Activity ID -> int
    :param access_token: Settings/My API Applications/Your Access Token -> str
    :return activity: -> dict
    """

    endpoint_url = "https://www.strava.com/api/v3/activities/{}".format(activity_id)

    r = requests.get(endpoint_url,
                     headers=authorization_header(access_token))

    if r.ok:

        activity = json.loads(r.text)

    else:

        logger.error('Retrieve Activity Failed with a reason {}'.format(r.reason))
        activity = None

    return activity


def retrieve_streams(activity_id, access_token, **kwargs):
    """Retrieve activity streams
    API V3: https://strava.github.io/api/v3/streams/#activity

    :param activity_id: Activity ID -> int
    :param access_token: Settings/My API Applications/Your Access Token -> str
    :param type: default=None, returns serialized original API response if set to 'original'
    :return streams: -> list
    """

    types = kwargs.get("types",
                       "time,latlng,distance,altitude,velocity_smooth,heartrate,cadence,watts,temp,moving,grade_smooth")

    endpoint_url = "https://www.strava.com/api/v3/activities/{}/streams/{}".format(activity_id, types)

    r = requests.get(endpoint_url,
                         headers=authorization_header(access_token))

    if r.ok:

        streams = json.loads(r.text)

    else:

        logger.error('Retrieve Streams Failed with a reason {}'.format(r.reason))
        streams = None

    if streams and not kwargs.get('type', None):

        streams = stream2dict(streams)

    return streams


def stream2dict(stream_list):
    """Convert stream list into stream dict

    :param stream_list: stream in list form, typical Strava API v3 response
    :return stream_dict: stream in dict form, ready to be consumed by pandas
    """

    stream_dict = {}

    for s in stream_list:

        stream_dict.update({s['type']: s['data']})

    return stream_dict


def zones2list(zones, type="power"):
    """Convert zones Strava response into a list

    :param zones: dict, Strava API zones response
    :param type: default="power", others "heart_rate"
    :return y: list, zones boundaries with left edge set to -1 and right to 10000
    """

    y = list(map(lambda x: x['min'], zones[type]["zones"]))
    y[0] = -1
    y.append(10000)

    return y


def authorization_header(access_token):
    """Authorization header dict to be used with requests.get()

    :param access_token: Settings/My API Applications/Your Access Token -> str
    :return header: -> dict
    """

    rv = {'Authorization': 'Bearer {}'.format(access_token)}

    return rv
