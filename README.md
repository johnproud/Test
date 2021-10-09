# Set up
## Commands to install virtual environment:
* python 3.9
* `pip install poetry`
* `poetry install`

## DB configuration
### 1. First of all you should configure .env file for configure project. You can see an example in .env.example file or just use command `cp .env.example .env` for initiaaliztion of configure file. Right now there is a postgresql backend for orm in case if you want to change this the following backends are available:

* django.db.backends.mysql ----> MySql
* django.db.backends.oracle -----> Oracle
* django.db.backends.sqlite3 -----> SqlLite
* django.db.backends.postgresql_psycopg2 ----> PostgreSql

### 2. Next you should migrate db structure and for this you have to use `python manage.py migrate`
### 3. If you want to have default admin user for this app then you should run `python manage.py loaddata seed/users.json`
### Credentials for this user are:
    * email: ```test@test.com```
    * password: ```test```

### 4. In order to start app you should run `python manage.py runserver`

### Swagger url: `http://localhost:8000` with documentation of endpoints
