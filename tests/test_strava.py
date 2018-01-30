from vmpy.strava import authorization_header
from vmpy.strava import stream2dict


def test_autorization_header():

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