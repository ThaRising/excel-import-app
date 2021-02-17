# BauerDude

This project was generated with
the Cookiecutter CLI,
using the **Drizm-Django-Template**.

## Setup

If you generated this project,
then all the actions listed below,
will have already automatically
been performed.

Otherwise,
you will need to add a file for
all the project related secrets.  
To file is expected to be located at
``BauerDude/settings/keys.py``

You must add the following variables:  
- ``SECRET_KEY = 'your-secret-key-here'``

For your convinience, these are
used during local development.  
You will however, have to add them
as environment variables for deployment.

## Development

To get started with local development,
run the following commands for a
quick setup:  
````bash
cd docker
docker-compose -p BauerDude up --build
poetry run python manage.py migrate
poetry run python manage.py runserver
````

This project includes a default
superuser.  
The development credentials are:  
- Email: "root@root.com"
- Password: "root"

You can change these in the
development settings file.

## Local Deployment

Before running these commands,
make sure all scripts have the
appropriate Linux LF carriage
characters in place.

To set up a local, dockerized
testing environment, do the following:  
````bash
vagrant up --provision
````

Startup may take around 1-2 mins
after the VM build has been completed.

The server should now be
available at ``localhost:30007``.

## Deployment

This project includes a full
setup for a pipeline
from development to Heroku.

The following environment
variables need to be set
for deployment:
- ``SECRET_KEY``
- ``ADMIN_EMAIL``
- ``ADMIN_PASSWORD``
- ``GSP_CREDENTIALS``
- ``GSP_INSTANCES``
- ``DATABASE_URL``
