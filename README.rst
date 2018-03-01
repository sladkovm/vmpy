=======================================
VMPY - Performance Velo Metrics Toolbox
=======================================

**VMPY** is a toolbox for evaluating *typical*
*Cycling Performance Metrics* from the ride data e.g. power, heart-rate, velocity,
gradient, cadence streams.

All functions within the package do follow the convention, where input/output
formats are either traditional *Python* built-in data structures
or are the *nd-arrays*. This design choice favors easy integration into other projects,
e.g. `velometria.com <http://velometria.com>`_

To help you getting started VMPY also provides a very thin wrapper around the
`Strava API <https://strava.github.io/api/>`_.


Installation
============

Official release:

``pip install vmpy``

The bleeding edge work in progress:

``pip install git+git://github.com/sladkovm/vmpy.git@development``


Scope
=====

The *VMPY* package provides the following functionality:

``metrics.py``: Cycling Performance Metrics

``preprocess.py``: Various clean-up tools e.g. handle moving=False and rolling means

``strava.py``: Python wrapper around the Strava API v3 for fetching Athletes, Activities and Stream data


Usage
=====

>>> from vmpy import strava
>>> stream = strava.retrieve_streams(activity_id=1282167861, access_token=STRAVA_ACCESS_TOKEN)


>>> from vmpy import metrics
>>> power_zones = metrics.zones(stream['watts'], ftp=270)
>>> hr_zones = metrics.zones(stream['heartrate'], lthr=160)
>>> best_1min = metrics.best_interval(stream['watts'], window=60)


>>> from vmpy import preprocess
>>> watts_3sec = preprocess.rolling_mean(stream['watts'], window=3, mask=stream['moving'])
>>> gradient_wo_outliers = preprocess.median_filter(stream['grade_smooth'], window=31, threshold=1)



>>> stream = strava.retrieve_streams(activity_id=1282167861, access_token=STRAVA_ACCESS_TOKEN)


>>> from vmpy import metrics
>>> power_zones = metrics.zones(stream['watts'], ftp=270)
>>> hr_zones = metrics.zones(stream['heartrate'], lthr=160)
>>> best_1min = metrics.best_interval(stream['watts'], window=60)


>>> from vmpy import preprocess
>>> watts_3sec = preprocess.rolling_mean(stream['watts'], window=3, mask=stream['moving'])
>>> gradient_wo_outliers = preprocess.median_filter(stream['grade_smooth'], window=31, threshold=1)



>>> stream = strava.retrieve_streams(activity_id=1282167861, access_token=STRAVA_ACCESS_TOKEN)


>>> from vmpy import metrics
>>> power_zones = metrics.zones(stream['watts'], ftp=270)
>>> hr_zones = metrics.zones(stream['heartrate'], lthr=160)
>>> best_1min = metrics.best_interval(stream['watts'], window=60)


>>> from vmpy import preprocess
>>> watts_3sec = preprocess.rolling_mean(stream['watts'], window=3, mask=stream['moving'])
>>> gradient_wo_outliers = preprocess.hampel_filter(stream['grade_smooth'], window=31, threshold=1)


Quick Start
===========

**Register Strava App**

In order to be able to use Strava API the user App must be registered at the `<link
http://www.strava.com/developers>`_:

*Application Name:* ex.: *My Awesome App*

*Website:* ex.: *myawesomeapp.com* (can be anything, even your FB or Strava page will do)

*Application Description* ex.: *Just fooling around with some Strava data*

*Authorization Callback Domain* *127.0.0.1* (unless you are building a serious App)

**Access Token**

The *Access Token* will be found at the `users profile page <https://www.strava.com/settings/api>`_
It will look like this: *83ebeabdec09f6670863766f792ead24d61fe3f9*

Access Token must be passed explicitly as an argument
to the functions found in ``strava.py`` module


Useful links
============

- Strava API v3 documentation - https://strava.github.io/api/
