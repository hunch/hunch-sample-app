Hunch Application Framework
================================

This application is a starting point for developers who want to build
applications using the [Hunch API](http://hunch.com/developers/). The
application is built to run on [Google App Engine](http://code.google.com/appengine/),
but can can also be used as a stand-alone Django project.

This sample application will display recommendations for a single
Hunch user by placing that user's AUTH_TOKEN in app/config.py. If you
would like to generate recommendations for arbitrary Hunch users,
obtain an APP_ID and APP_SECRET by e-mailing [bd@hunch.com](mailto:bd_hunch.com). You will
them be able to Hunch connect (OAuth) users into your application and
store their auth_tokens.

Other libraries used include:
* jQuery JavaScript Framework [http://jquery.com/](http://jquery.com/)
* Mustache JavaScript templating library [http://github.com/janl/mustache.js](http://github.com/janl/mustache.js)
* Hunch JavaScript SDK [http://hunch.com/developers/v1/resources/samples/](http://hunch.com/developers/v1/resources/samples/)
* Google App Engine Helper for Django [http://code.google.com/p/google-app-engine-django/](http://code.google.com/p/google-app-engine-django/)


Getting started
---------------

1. Download [Google App Engine Python SDK](http://code.google.com/appengine/downloads.html)

2. Configure initial settings
   * in app/config.py, edit APP_ID and APP_SECRET for your Hunch application, OR
   * in app/config.py, add your AUTH_TOKEN for the test page to function. Your AUTH_TOKEN can be found at [the bottom of the Hunch developer docs](http://hunch.com/developers/v1/docs/) (login and select "show my auth_token")
   * if you're using GAE: in app.yaml, edit app-name; in app/config.py, edit APP_HOSTNAME

3. Update the settings.py file
   * in settings.py, edit ADMINS and SECRET_KEY

4. Test your app loads the test page
   * run `python dev_server.sh` (this defaults to running on port 80 which may require root permissions)
   * open a web browser and navigate to [http://localhost](http://localhost)
   * ensure that you see the success page
   * now navigate to [http://localhost/app/](http://localhost/app/)
   * ensure that you see the recommendations being populated correctly

5. When ready, deploy the app to GAE
   * `python manage.py update`


Useful commands
---------------

Start the development server
`sh dev_server.sh`

Start the development server with a fresh datastore
`sh fresh_dev_server.sh`

Publish your app to GAE
`python2.5 manage.py update`

Launch a local Python console for interecting with the app and datastore
`python2.5 manage.py shell`

Launch a remote Python console for interacting with the app and datastore
`python2.5 manage.py console APP_NAME`


Notes and gotchas
-----------------

* GAE will penalize your app if requests take over 1000 ms to complete, so
push as many calls to the frontend as possible by using the
[Hunch Javascript SDK](http://hunch.com/media/js/hunch-api.js)

* This application is packaged with [google-app-engine-django](http://code.google.com/p/google-app-engine-django/), a helper
for creating Django projects that run on GAE. It is worthwhile to read
the [overview of using the helper](http://code.google.com/appengine/articles/appengine_helper_for_django.html).
A zip file of Django 1.0.2 is included as django.zip to be used by the
helper

* GAE uses Python 2.5, so running scripts like `manage.py` with python2.5 is
recommended. The scripts `dev_server.sh` and `fresh_dev_server.sh` also use python2.5

* For testing, it is useful to redirect your-app-name.appspot.com to your local machine.
To accomplish this, edit your /etc/hosts file and point that address to your IP (or localhost)
