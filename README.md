# Velometria.py

## Purpose

This hobby project is a combination of my passion for cycling and interest in quantitative sports 
physiology. It also serves as a platform for improving my Python programming skills resulting in heavy 
usage of Object Oriented Programming and Test Driven Development approaches  (in contrast to what 
I have to use with scientific Python at my daily job as a physics engineer)


## Scope

The *Velometria.py* library provides the following functionality:

* Python wrapper around the Strava API v3 for fetching Athletes and Activities data
* Library for calculating and visualising various sport performance metrics (see methods of Activity and CompareActivities classes)
* Support for mongodb import/export that can be used in combination with a Meteor.js app (will be added soon)


## Usage


### Register Strava App

In order to be able to use Strava API the App must be registered at http://www.strava.com/developers
It is easier than it sounds and typical registration settings will be:


**Application Name:** *My Awesome App*

**Website:** *myawesomeapp.com* (can be anything, even yout FB or Strava page will do)

**Application Description** *Just fooling around with some Strava data*

**Authorization Callback Domain** *127.0.0.1* (unless you are building a serious App)


### Athlete (Your) ID and Access Token
 
* To get the Athlete ID simply go to your Strava page https://www.strava.com/athletes/227615 where 
last digits will represent the actual ID. In this case it is *id=227615*

* Your Access Token will be found at https://www.strava.com/settings/api
It will look like this: *83ebeabdec09f6670863766f792ead24d61fe3f9*


### Setting Up the Python App

In order to get the Python App working create in the root folder of the App the file *./config/athlete.config*
with the following content:

```
{
  "athlete_id": "227615",
  "access_token": "83ebeabdec09f6670863766f792ead24d61fe3f9"
}
```

Sharp eye wll recognize here a simple JSON object with two key-value pairs: *athlete_id* and *access_token*. Both
 were retrieved in the previous step.


### [Advanced] Client ID and Secret

In case you are developing a multi-user app you will need a *Client ID* and a *Secret*. These two parameters can be used
for requesting user to authorize the permission to his data - essentialy to give you an *access_token*.

Wrapper around the Authentication process is implemented in *strava/client.py* library. To get it working, the 
*./config/client.config* file must be created with following content:

```
{
  "client_id": "9",
  "client_secret": "7b2946535949ae70f015d696d8ac602830ece412"
}
```


## Use cases

The folder cases provides an example of App usage for visualizing and comparing two rides. The example is provided in iPython 
(a.k.a. Jupyter) notebook

## Useful links

- Strava API v3 documentation - https://strava.github.io/api/
- Workable, extensive and professionaly made Python wrapper around the Strava API - https://github.com/hozn/stravalib


## Contributions

Despite the hobby nature of this project it is by all means open for pull, issues and ideas requests. 
Comments regarding coding style and best programming practices are welcome as well.