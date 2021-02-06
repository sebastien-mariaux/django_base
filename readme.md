
# DJANGO BASE

A standard base for a django project.


## Included features
### Fonctionnalities
- Custom user model with email authentication

### Testing and quality of code
- Pytest


## Setup
Postgres database run in a docker container:

`docker-compose up`

Lauch the virtual environement and install modules:

```
workon django_base
pip install -r req.txt
```

### Automation test
sudo apt-get install chromium-browser

cd /usr/bin
sudo CHROME_VERSION=$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
sudo wget https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip
sudo unzip chromedriver_linux64.zip 
sudo chmod +x /usr/bin/chromedriver
