# Run Tracker

## A **Highly** Specialised Run Data Viewer ##

When I started running I tracked my routes by way of a phone strapped to my arm.
A phone with incredibly creative GPS.  The results were at best sketchy and at worst bearing no relation to reality.

Then I got a Garmin watch and my life (and run accuracy) improved accordingly.

I needed a way to visualise my progress over time, and to try and make sense of the erratic results my phone had given me.  So I decided to use the Python Chain of Resposibility data structure, TDD and pandas to handle and visualise all the data I'd accumulated.

The result is a rather beautiful graph with a definite trend.  Turns out all those early starts weren't for nothing - I'm getting faster!  (Yes, okay, I'm still quite slow.  But I'm faster than I was!)

This repo is just for show really (had to hide my sweet sweet mapmyrun credentials...) so I've included a png of the output.


# runTracker

### Run Data Handler ###

A module to take raw run data and test its validiy.
If valid and certain conditions are met the distances will 
be adjusted due to inaccurate GPS recording.

If the data is valid it returns the data in dictionary form.
If the data is not valid it returns None

Stages of checking data:
    
-   Is data valid?  Is it a dict with the REQUIRED_DATA_PARAMS?
    if yes, continue.
    If no, return None.

-   Is it a run (outdoor or treadmill)?
    If yes, continue.
    If no, return None.

-   Is this a treadmill run?
    If yes create Run based on data given.
    If no, continue.

-   Is the run from before or after GARMIN_DATE?
    If before, continue.
    If no, create Run based on exact data given.

-   Is run below MINIMUM_RUN_DISTANCE?
    If yes, return None.
    If no, continue.

-   Is the date before HOUSEMOVE_DATE?
    If yes, return Run with HOUSEMOVE_DISTANCE.
    If no, continue.

-   Is the date before FIVE_KM_START_DATE?
    If yes, return Run with exact distance.
    If no, pass to default handler.

-   Is the date after the LOCKDOWN_DATE and over 6km?
    If yes, if over 6km - return Run with POST_LOCKDOWN_DISTANCE.
    If no, continue.

-   Is the run over 6km?
    If yes, return Run with long Brentwood run distance.
    If no, continue.

-   Default Handler:
    We know it's a valid outdoor run after HOUSEMOVE_DATE and before
    LOCKDOWN_DATE, longer than MINIMUM_RUN_DISTANCE and shorter 
    than LONG_RUN_THRESHOLD.
    Return Run with short SHORT_RUN_DISTANCE.

