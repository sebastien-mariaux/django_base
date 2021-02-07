echo 'PYCODESTYLE'
pycodestyle django_base
pycodestyle users


echo 'MYPY'
mypy --config-file tox.ini django_base
mypy --config-file tox.ini users


echo 'PYLINT'
pylint -j0 users
pylint -j0 django_base

