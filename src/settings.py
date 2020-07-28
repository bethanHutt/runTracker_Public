import datetime

### GRAPH SETTINGS ###

GRAPH_SIZE = (12,8)
GRAPH_FORMAT = 'ro'

### WEB SCRAPING SETTINGS ###

URL = 'https://www.mapmyrun.com'
LOGIN_URL = URL + '/auth/login'
WORKOUT_URL = URL + '/workouts/dashboard.json?month={month}&year={year}'
START_YEAR = 2019
CURRENT_YEAR = datetime.datetime.now().year + 1


#### DATA SETTINGS ###

DATE_DELIMITTER = '-'

REQUIRED_DATA_PARAMS = [
    'date',
    'activity_short_name',
    'distance',
    'time',
]

VALID_ACTIVITY_TYPES = [
    'run',
    'indoorrun',
]

MINIMUM_RUN_DISTANCE = 2.8

FIVE_KM_START_DATE = (2019, 8, 3)

HOUSEMOVE_DATE = (2019, 6, 1)
HOUSEMOVE_DISTANCE = 3.10

LOCKDOWN_DATE = (2020, 3, 23)
POST_LOCKDOWN_DISTANCE = 6.6

LONG_RUN_THRESHOLD = 5.58
LONG_RUN_DISTANCE = 6.97

SHORT_RUN_THRESHOLD = 5
SHORT_RUN_DISTANCE = 5.29

BAD_RUN_DATE = (2020, 5, 21)

GARMIN_DATE = (2020, 7, 1)
