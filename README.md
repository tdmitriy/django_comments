# Django web app with threaded comments and facebook authorization via [allauth](https://github.com/pennersr/django-allauth)


[![Build Status](https://travis-ci.org/tdmitriy/django_comments.svg?branch=master)](https://travis-ci.org/tdmitriy/django_comments)

## How to setup
1. `git clone` and go to the project folder
2. setup your virtualenv `virtualenv env`
3. install project libs/frameworks `pip install -r requirements.txt`
4. run django migrations `python manage.py migrate`
5. create superuser `python manage.py createsuperuser`
6. follow allauth [instructions](https://django-allauth.readthedocs.io/en/latest/installation.html) and setup your project
7. next you need to create aplication in facebook deveoper [account](https://developers.facebook.com/) and configure it.
8. after that, you need to go to the django admin panel and change the existing site in `Site` model from `example.com` to your project url, for example `localhost:8000`
9. in the current admin panel go to the `Social application model` and select your site from prev step and then configure it with your facebook `app id`, `secret key` and poll down your site from `Available sites` to `Choosen sites`. Save.
10. That's it.


Working [DEMO](http://haswell.pythonanywhere.com/)