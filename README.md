# iReporter

[![Build Status](https://travis-ci.org/izo30/iReporter.svg?branch=develop)](https://travis-ci.org/izo30/iReporter) [![Coverage Status](https://coveralls.io/repos/github/izo30/iReporter/badge.svg?branch=ch-add-tests-162368098)](https://coveralls.io/github/izo30/iReporter?branch=ch-add-tests-162368098) [![Maintainability](https://api.codeclimate.com/v1/badges/ef698b481f64d9160d87/maintainability)](https://codeclimate.com/github/izo30/iReporter/maintainability)

A system for reporting any form of corruption to the appropriate authorities and seeking for government intervention on important issues.

## Available Endpoints:

| Http Method | Endpoint Route | Endpoint Functionality
| --- | --- | --- |
| `POST` | /api/v1/auth/login | Login a user |
| `POST` | /api/v1/auth/signup | Signup a user |
| `POST` | /api/v1/incidents | Create a new incident |
| `GET` | /api/v1/incidents | Get all incidents |
| `GET` | /api/v1/incidents/admin | Admin get all incidents |
| `PUT` | /api/v1/incidents/admin/incident_id | Edit incident status |
| `PUT` | /api/v1/incidents/incident_id | Edit an incident |
| `DELETE` | /api/v1/incidents/incident_id | Delete a specific incident |
| `GET` | /api/v1/incidents/incident_id | Get a specific incident |

## Prerequisites

```
- pip
- virtualenv
- python 3 or python 2.7
```

## Installation
Clone the repo
```
git clone https://github.com/izo30/iReporter.git
```
Create a virtual environment
```
virtualenv <environment name>
```
Activate the environment
```
$source <your environment name>/bin/activate
```
Install dependencies
```
$pip install -r requirements.txt
```
Run the app
```
python run.py
```

## Running the tests
The tests have been written using the python module unittests. The path to tests folder is app/tests/v1 for version 1 tests only. Use a test framework like pytest to run the tests. Use the command:
```
pytest app/tests/v1
```

## Deployment
The api is deployed on heroku on [THIS](https://kbucket-api-heroku-ireporter.herokuapp.com/api/v1/ "Heroku Link") link

## Built with
Flask, a python framework

## Authors
[Isaac Wangethi](https://github.com/izo30 "Isaac Wangethi")
