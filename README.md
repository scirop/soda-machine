# soda-machine

[![CircleCI](https://circleci.com/gh/scirop/soda-machine.svg?style=svg)](https://circleci.com/gh/scirop/soda-machine)

A simple flask_sqlalchemy based web-app to add/remove soda machines
and add/remove sodas from the soda Machines

Credits to [Jennie](https://github.com/jennielees/flask-sqlalchemy-example) for the simple
flask_sqlalchemy example app.


Developed for Python3

### Assumptions:
1. Machine names are case sensitive, e.g. Machine1 and machine1 would be treated as different machines
2. Machine names must have alphanumeric characters included
3. Soda names are case sensitive
4. Soda names must have alphanumeric characters included
5. In case the soda is repeated, we add a numeric suffix, e.g. pepsi_1, pepsi_2 etc
6. Soda names are entered manually for creation and deletion operations

Run the following before spinning up the app, to create the initial db

```
python3 models.py
```

Run the following for subsequent runs

```
python3 app.py
```

Hosted on [Heroku](https://soda-machine.herokuapp.com)
