=======================================
VMPY - Performance Velo Metrics Toolbox
=======================================

**VMPY** toolbox focuses on providing a comprehensive collection of *typical*
*Cycling Performance Metrics*.

All functions within the package do follow the convention, where input/output
formats are either traditional *Python* built-in data structures
or are the *nd-arrays*. This design choice favors easy integration into other projects,
e.g. [velometria.com](http://velometria.com).

*VMPY* provides a very thin wrapper around
 the [Strava API](https://strava.github.io/api/ to help you getting started.

Scope
=====

The *VMPY* package provides the following functionality:

```metrics.py```: Cycling Performance Metrics

```preprocess.py```: Various clean-up tools e.g. handle moving=False and rolling means

```strava.py```: Python wrapper around the Strava API v3 for fetching Athletes, Activities and Stream data

Quick Start
===========

1. Register Strava App

In order to be able to use Strava API the user App must be registered at http://www.strava.com/developers
It is easier than it sounds and typical registration settings will be:


*Application Name:* ex.: *My Awesome App*

*Website:* ex.: *myawesomeapp.com* (can be anything, even your FB or Strava page will do)

*Application Description* ex.: *Just fooling around with some Strava data*

*Authorization Callback Domain* *127.0.0.1* (unless you are building a serious App)

2. Access Token

Your *Access Token* will be found at https://www.strava.com/settings/api
It will look like this: *83ebeabdec09f6670863766f792ead24d61fe3f9*

Access Token must be passed explicitly as an argument
 to the functions found in ```strava.py``` module

Useful links
============

- Strava API v3 documentation - https://strava.github.io/api/
