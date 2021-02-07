echo 'RUN TESTS...'
coverage run --source='.' manage.py test users

echo 'GENERATE COVERAGE...'
coverage report
coverage html


echo 'RUN PYCODESTYLE...'
pycodestyle django_base
pycodestyle users


echo 'RUN MYPY'
mypy --config-file tox.ini django_base
mypy --config-file tox.ini users


echo 'RUN PYLINT'
pylint -j0 users
pylint -j0 django_base

