from vmpy.strava import authorization_header
from vmpy.strava import stream2dict
from vmpy.strava import zones2list


def test_authorization_header():

    access_token = 'abc123'
    expected = {'Authorization': 'Bearer abc123'}

    assert authorization_header(access_token)==expected


def test_stream2dict():

    stream_list = [
        {
            "data": [1,2,3],
            "type": "numbers"
        },
        {
            "data": ['a', 'b', 'c'],
            "type": "letters"
        }
    ]

    expected = {
        "numbers": [1, 2, 3],
        "letters": ["a", "b", "c"]
    }

    assert stream2dict(stream_list) == expected


def test_zones2list_power(test_zones):

    rv = zones2list(test_zones, type="power")
    expected = [-1, 144, 196, 235, 274, 313, 391, 10000]
    assert rv == expected


def test_zones2list_heart_rate(test_zones):

    rv = zones2list(test_zones, type="heart_rate")
    expected = [-1, 142, 155, 162, 174, 10000]
    assert rv == expected
