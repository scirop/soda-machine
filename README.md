# soda-machine

[![CircleCI](https://circleci.com/gh/scirop/soda-machine.svg?style=svg)](https://circleci.com/gh/scirop/soda-machine)

A simple web-app to add/remove soda machines and add/remove sodas from the soda Machines

Basic code inspiration source -- [Jennie](https://github.com/jennielees/flask-sqlalchemy-example)


Developed for Python3

### Assumptions:
1. Machine names are case sensitive, e.g. Machine1 and machine1 would be treated as different machines
2. Machine names must have alphanumeric characters included
3. Soda names are case sensitive
4. Soda names must have alphanumeric characters included
5. In case the soda is repeated, we add a numeric suffix, e.g. pepsi_1, pepsi_2 etc
6. Soda names are entered manually for creation and deletion operations

Run the following command if the application is being run for the first time

```
python3 app.py create
```

Run the following for subsequent runs

```
python3 app.py
```

Hosted on [Heroku](https://soda-machine.herokuapp.com)
