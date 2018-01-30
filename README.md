# VMPY - Cycling Performance Metrics in Python

**VMPY** *(read as ```wimpy [kid]```)* provides tools for calculating *typical*
**Cycling Performance Metrics** from
the ride data collected by cycling computers e.g. Garmin,
or fetched from the fitness trackers e.g. Strava.

The package itself does not implement parsing or REST client
(except for a very thin wrapper around the
 [Strava API](https://strava.github.io/api/) to get you started),
but rather encourages to use it as a part of data analysis workflow.
In fact, the **VMPY** calculations are used to power the [velometria.com](http://velometria.com)

The main design constraint respected in all the **VMPY** functions is to limit the input/output formats to traditional
*Python* built-in data structures or *nd-arrays* to facilitate easy integration into other projects.

## Scope

The *VMPY* package provides the following functionality:

```metrics.py```: Cycling Performance Metrics

```preprocess.py```: Various clean-up tools e.g. handle moving=False and rolling means

```strava.py```: Python wrapper around the Strava API v3 for fetching Athletes, Activities and Stream data

## Quick Start

### Register Strava App

In order to be able to use Strava API the user App must be registered at http://www.strava.com/developers
It is easier than it sounds and typical registration settings will be:


**Application Name:** ex.: *My Awesome App*

**Website:** ex.: *myawesomeapp.com* (can be anything, even your FB or Strava page will do)

**Application Description** ex.: *Just fooling around with some Strava data*

**Authorization Callback Domain** *127.0.0.1* (unless you are building a serious App)

### Access Token

Your Access Token will be found at https://www.strava.com/settings/api
It will look like this: *83ebeabdec09f6670863766f792ead24d61fe3f9*

Access Token must be passed explicitly as an argument
 to the functions found in ```strava.py``` module

## Useful links

- Strava API v3 documentation - https://strava.github.io/api/
