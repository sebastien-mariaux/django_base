


# DJANGO BASE

A standard base for a django project.


## Included features
### Functionalities
- Custom user model with email authentication
- Basic Account interface with profile edition
- Base layout using Bootstrap
- Basic markdown integration

### Testing and quality of code
- Pytest
- Pycodestyle
- Mypy
- Pylint
- Coverage

Run with `./pipeline.sh`

## Setup
### Backend
Postgres database run in a docker container.

First change the database port in both `docker-compose.yml` and django `settings.py` file. This avoid conflicts between projects running on the same local environment.

Then run:

`docker-compose up`

Install prerequisites:
`sudo apt install libpq-dev`

Launch the virtual environment and install modules:

`workon django_base`

`pip install -r req.txt`

Replace all occurrences of `django_base` by your own project name. Don't forget to also rename the django_base folder.

### Frontend
Frontend running with webpack and babel.

Make sure you have node and npm installed.

Your frontend code should be in the `assets` folder. It will be compiled to the `static` folder.
Run `npm install`
Run `npm run dev` to process asset in development mode

### Fixtures
Install :
`./manage.py loaddata django_base/fixtures/users.json`

Admin user :

- username : capitain.raymond.holt@b99.com
- password : iamthebossofthe99

Normal user :

- username : jake.peralta@b99.com
- password : rosa1234

Alternatively, create a custom superuser :
`./manage.py createsuperuser`

Or create your own fixtures!

## Helpfull documentation

[Documentation Django](https://docs.djangoproject.com/)

[Django and frontend integration](https://www.saaspegasus.com/guides/modern-javascript-for-django-developers/integrating-javascript-pipeline/)
