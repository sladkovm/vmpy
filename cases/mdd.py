from strava import athlete
from strava import activity

athlete = athlete.Athlete()

id_mdd28 = '163301368'
id_mdd30 = '628508858'

mdd28 = activity.Activity(athlete=athlete, activity_id=id_mdd28)
mdd30 = activity.Activity(athlete=athlete, activity_id=id_mdd30)

