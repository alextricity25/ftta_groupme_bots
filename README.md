# Python: FTTA GroupMe Bots

A Django/Heroku application that runs several useful GroupMe bots for the FTTA.

1) Runs a bot that randomly chooses a hymn from the UK YP Songbook and posts it to the group
2) Runs celery, which allows periodic tasks to post messages to GroupMe for Roll Call purposes
3) Has a celery task that grabs a psudo-random verse from online.recoveryversion.org and posts it to the GroupMe group


TODO:
1) Maintains a list of class memory verses, runs study_it.py on them, and posts them to the GroupMe group.
2) Maintains a database of all the class readings on a per week basis. These readings can be referenced with the '#showmethereading <class>' hashtag. The bot will respond with the current weeks reading assignments.
3) Add search funtionality when choosing a song from the YP songbook. That way someone could reference a song using '#sendsong pattern' hashtag. The bot would then send the song with chords that has lyrics that match that pattern.

4) Update this read me with instructions on how to deploy this bot
