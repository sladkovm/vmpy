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
