# Django CircleCi Example

## The Project
The idea behind this project is an app to help keep track of physical media, but really it is just an example project to have something to test and build in CircleCi.

## Local Setup for the Application

### Dependencies

- Python
- Postgresql
- pip

## Setup

1. Create a virtual env and activate it.

```bash
python -m venv venv
source venv/bin/activate
```

2. Install the Dependencies.

`pip install -r requirements.txt`

3. Create a database and a database user.
```bash
createdb my_media
psql my_media
my_media=> CREATE ROLE example WITH LOGIN CREATEDB PASSWORD '1234';
```

4. Run the migrations.

`python manage.py migrate`

## The Tests
There are a few unit tests that can be run with:

`python mangae.py test`

## Run Pylint

`pylint my_media/ media_organizer/`
