
# DJANGO BASE

A standard base for a django project.


## Included features
### Fonctionnalities
- Custom user model with email authentication

### Testing and quality of code
- Pytest
- Pycodestyle
- Mypy
- Pylint
- Coverage

Run with `./pipeline.sh`

## Setup
Postgres database run in a docker container:

`docker-compose up`

Lauch the virtual environement and install modules:

```
workon django_base
pip install -r req.txt
```

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