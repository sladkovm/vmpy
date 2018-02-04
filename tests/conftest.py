import os
import pytest
import json
from vmpy import strava


@pytest.fixture
def test_stream():

    _here = os.path.abspath(__file__)

    f_name = os.path.normpath(os.path.join(_here, '../assets/streams_1202065_1354978421.json'))
    with open(f_name) as f:

        _stream = json.load(f)

        return strava.stream2dict(_stream)


@pytest.fixture
def test_stream_with_nans():

    _here = os.path.abspath(__file__)

    f_name = os.path.normpath(os.path.join(_here, '../assets/streams_1202065_1299011495.json'))

    with open(f_name) as f:

        _stream = json.load(f)

        return strava.stream2dict(_stream)


@pytest.fixture
def test_zones():

    rv = {
        'heart_rate': {'custom_zones': True,
                        'zones': [{'max': 142, 'min': 0},
                                  {'max': 155, 'min': 142},
                                  {'max': 162, 'min': 155},
                                  {'max': 174, 'min': 162},
                                  {'max': -1, 'min': 174}]},
             'power': {'zones': [{'max': 143, 'min': 0},
                                 {'max': 195, 'min': 144},
                                 {'max': 234, 'min': 196},
                                 {'max': 273, 'min': 235},
                                 {'max': 312, 'min': 274},
                                 {'max': 390, 'min': 313},
                                 {'max': -1, 'min': 391}]}}

    return rv