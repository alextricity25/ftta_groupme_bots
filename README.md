# Python: Consider, Incite, Exhort (CIE) - Heb. 10:24-25


# Goal:
And let us consider one another so as to incite one another to love and good works, not abandoning our own assmebling together, as the custom with some is, but exhorting one another; and so much the more as you see the day drawing near. - Hebrews 10:24-25

The goal of this Heroku Django application is to help Christians all over the
world foster an atmosphere of considering, inciting, and exhorting one another,
especially in the group meetings. The Bible shows us that the early believers
met from "house to house"(Acts 5:42, 2:46), partaking of their food with exultation
and simplicity of heart.

CIE is a simple django application that runs on a heroku dyno. It hooks up to
the GroupMe communication app to assist with the coordination, schedule, and
other practical matters involved in a group meeting.

This application has been designed with the view to aide such a fostering of mutual teaching, love,
 and care among God's children. It by no means should be used to replace the function of the believers,
but rather as a tool to help the Christian small group meetings.

Ideas:
* Maintain a schedule of home rotations for the small group meetings. That schedule can then
  be referenced using the '#showschedule' hastag.
* Runs a GroupMe bot that sends a reminder of the weekly small group gathering, also sending
  some info about the time, location, and maybe suggestions on what to bring.
* Send a random memory verse with the reminder
* Head counter? People who know for sure that they are coming can assist the host with a head
  count by responding with the '#yes' hashtag, or maybe use a groupme poll?

# Description:

A Django/Heroku application that runs several useful GroupMe bots

This application currently has the following features:

1) Runs a bot that listens for the "#sendsong" hashtag. If it's caught, then the bot will
   send a random song from the UK YP songbook.
2) Runs celery, which allows periodic tasks to post messages to GroupMe for Roll Call purposes
3) Has a celery task that grabs a psudo-random verse from online.recoveryversion.org and posts it to the GroupMe group. A groupme bot can then be used to post the verse.
4) Maintains a list of verses in the database. The list of verses can be adjusted via the
   admin panel. In addition, the application provides an endpoint, '/memory_verses', that listens
   for a POST request with a text body that contains the string '#memoryverse'. When the string
   is encountered, the app will post a random verse from the memory verse list to a 
   groupme group using a groupme bot. TODO: Add more documentation on this. Especially on how
   to set the proper env variables for the groupme bot to work.


TODO:
* Add search funtionality when choosing a song from the YP songbook. That way someone could reference a song using '#sendsong pattern' hashtag. The bot would then send the song with chords that has lyrics that match that pattern.

* Update this read me with instructions on how to deploy this bot


# Instructions on how to deploy the app on heroku:

1. Clone this repository
```
git clone https://github.com/alextricity25/ftta_groupme_bots.git
```

2. Follow the instructions provided by heroku on how to authenticate
   and set up a new project:
   https://devcenter.heroku.com/articles/getting-started-with-python#introduction

Take note that you can skip the step asking you to clone the getting started project.
This is because we don't want to start a new project, but rather deploy an existing one.

3. Add the Heroku apt experimental buildpack:
```
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-apt
```
This is needed to install some essential packages on the Heroku dyno.


4. Push the repository to your heroku app repository.
After taking care of the prerequisites listed on Heroku's getting started guide, you can now
create a heroku project and push the application up to heroku for deployment:
```
$ heroku create
$ git push heroku master
```

You can run the command `heroku logs -t` to view the logs related to the app
deployment. You can also ensure that at least one instance of the app is
running with the command:
```
$ herkou ps:scale web=1
```

# Set up a GroupMe Bot:

Now that heroku django app is running, it's time to setup a GroupMe bot
with a callback URL to the app.

1. Ensure you have a GroupMe account. Login to the GroupMe Developer Portal:
   https://dev.groupme.com/

2. Go to the "Bots" tab, then choose "Create Bot"

  * Choose the group this bot will operate in.
  * Name the Bot
  * For the callback URL, you are going to use the heroku URL for the
    application that we deployed earlier. To get the URL, navigate
    to the project's directory tree, then run:
    ```
    heroku apps:info
    ```
    Append the URL with the path '/pick_a_song'. This is the URL that handles
    requests to choose a random song from the UK YP songbook.

After the bot has been created, take note of the "Bot ID".

3. Get your access token.
   To send a song, the FTTA bot utilizes the groupme image service. Before the bot can
   use the image service, it must have an access token configured. To obtain an access
   token, follow the provided instructions from groupme:
   https://dev.groupme.com/tutorials/oauth


3. Configure the Bot ID and access token environment variable on your Heroku dyno.
```
$ heroku config:set GROUPME_ACCESS_TOKEN=your-groupme-access-token
$ heroku config:set BOT_ID=your-bot-id
```

4. Restart the application:
```
heroku ps:restart web.1
```
