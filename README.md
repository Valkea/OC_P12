# EpicEvents

This project aims to provide a Customer Relationship Management app (or CRM)

Using the various endpoints the users will be able to manage events along with their related clients and contracts.


## Installation

In order to use this project locally, you need to follow the steps below:

### First, 
let's duplicate the project github repository

```bash
>>> git clone https://github.com/Valkea/OC_P12.git
>>> cd OC_P12
```


### Secondly,
let's create a virtual environment and install the required Python libraries

(Linux or Mac)
```bash
>>> python3 -m venv venv
>>> source venv/bin/activate
>>> pip install -r requirements.txt
```

(Windows):
```bash
>>> py -m venv venv
>>> .\venv\Scripts\activate
>>> py -m pip install -r requirements.txt
```


### Thirdly,
we need to connect with your local PostgreSQL. (If it is not installed yet, please visit the [official website](https://www.postgresql.org/download/) and follow the instructions for your current operating system to install and run PostgreSQL)

Create a database named `epic_events_crm`
```bash
>>> psql
>>> CREATE DATABASE epic_events_crm;
CREATE DATABASE
>>> \c epic_events_crm 
You are now connected to database "epic_events_crm" as user "xxxx".
>>> \q
```

Then create a `secrets.txt` file at the root of the project (in OC_P12)
1. on the first line put the `username`
2. and on the second line put the `password`

### Finally,

run the migration and initialize some data with the following command to run fixtures
```bash
>>> python manage.py migrate
>>> python manage.py loaddata apps/users/fixtures/demo_users.json
```

## Running the project

Once installed, the only required command is the following one

```bash
>>> python manage.py runserver
```


## Using the project

### as a user of the API

visit *http://127.0.0.1:8000/login/* and use the one of the demo credentials below:

> Manage Team
*demo-login :* manage_user
*demo-password :* demopass

> Sales Team
*demo-login :* sales_user
*demo-password :* demopass

> Support Team
*demo-login :* support_user
*demo-password :* demopass

> No Team
*demo-login :* noteam_user
*demo-password :* demopass

> Superadmin
*demo-login :* epicadmin
*demo-password :* demopass

**these accounts need to be removed / changed before going into production !**

#### then read the API documentation

the API documentation introduce the available endpoints with many examples and the expected HTTP status code.
*https://documenter.getpostman.com/view/13202435/Tz5qYwY2*

#### and test using the Postman of directly by browsing the API.

the easiest way to test the endpoints once the local server is running is by using them in Postman.

However, you can also browse the API directly in your browser as long as you provide a valid JWT token in the header (except for signup).
- This can be done in many ways, such as using the 'ModHeader' browser plugin (widely available).
- In this case, once installed, create an "Authorization" key and set the value as "JWT token" (where token is the access token returned when logging-in).
- Then the API can be visited just like a simple website (as long as the token is valid and the user has right to use the endpoint).

### as a user of the admin (front-end)

visit *http://127.0.0.1:8000/zadmin* and use the credential previously provided.

Once in the admin, you will be able to add, edit or remove 'clients', 'contracts', 'events', 'epic members' and even 'status' with the right account. The permissions should be the same as with the API itself.


## Tests
Unit tests were written in order to test the models & permissions.

You can run all the tests with the following command
```bash
>>> python manage.py test apps
```
**Warning**
Don't run `unittest` directly, use the Django's manager.


## Coverage

In order to see how well we're testing, [coverage](https://coverage.readthedocs.io/en/coverage-5.1/) was installed.

First we need to run the tests **with the coverage** module using the following command line

```bash
>>> coverage run --source='apps' manage.py test apps
```

Then we can produce an HTML report *(available in htmlcov)* with
```bash
>>> coverage html
```

Or simply print the result in the Terminal using
```bash
>>> coverage report
```

The overall coverage of the current version is about 91% at the moment.


## Documentation

The applications views are documented using the Django admindoc format.

However the admindoc module is not activated at the moment.

Also, the Postman API documentation is available here: 

*https://documenter.getpostman.com/view/13202435/Tz5qYwY2*


## PEP8

The project was developped using 'vim-Flake8' and 'black' modules to enforce the PEP8 rules.


## License
[MIT](https://choosealicense.com/licenses/mit/)
