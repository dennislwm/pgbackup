# pgbackup

Test driven development ["TDD"] of a PostgreSQL CLI backup tool to AWS S3 or locally.

<!-- TOC -->

- [pgbackup](#pgbackup)
  - [Project](#project)
    - [Setting up PostgreSQL server](#setting-up-postgresql-server)
    - [Installing PostgreSQL 9.6 client](#installing-postgresql-96-client)
    - [Testing connection from Workstation](#testing-connection-from-workstation)
    - [Creating the Virtualenv](#creating-the-virtualenv)
  - [Project Structure](#project-structure)
  - [Test Driven Development](#test-driven-development)
    - [Mocking in Test](#mocking-in-test)
    - [Storage](#storage)
  - [Usage](#usage)
    - [Workstation](#workstation)
    - [Production](#production)
  - [Packaging](#packaging)
    - [Generating a Wheel](#generating-a-wheel)

<!-- /TOC -->

## Project

Create a CLI tool that we can use to easily back up a PostgreSQL database to either AWS S3 or locally. The parameters are:

1. Database URL to backup
2. Driver (either `local` or `S3`)
3. Backup destination (a file path for `local` or a bucket name for `S3`)
4. Schema (optional dump schema only, not data)

### Setting up PostgreSQL server

Before we begin, we're going to need a PostgreSQL database to work with. The code repository contains a `db_setup.sh` script that we'll use on a CentOS 7 cloud server to create and run our database.

Create a CentOS 7 cloud server and run the following on it:

```bash
$ curl -o db_setup.sh https://raw.githubusercontent.com/linuxacademy/content-python3-sysadmin/master/helpers/db_setup.sh
$ chmod +x db_setup.sh
$ ./db_setup.sh
```

### Installing PostgreSQL 9.6 client

On our development machine, we'll need to make sure that we have the Postgres client installed. The version needs to be 9.6.6.

On Red-hat and CentOS systems we'll use the following:

```bash
$ wget https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
$ sudo yum install -y pgdg-redhat-repo-latest.noarch.rpm
$ sudo yum update -y
$ sudo yum autoremove -y postgresql
$ sudo yum install -y postgresql96
```

On Debian systems, the equivalent would be:

```bash
$ sudo apt-get install postgres-client-9.6
```

### Testing connection from Workstation

Let's make sure that we can connect to the PostgreSQL server from our development machine by running the following command:

*Note: You'll need to substitute in your database values for [USERNAME], [PASSWORD] and [SERVER_IP].*

```bash
$ psql postgres://[USERNAME]:[PASSWORD]@[SERVER_IP]:80/sample -c "SELECT count(id) FROM employees;"
```

### Creating the Virtualenv

We'll start by cloning this repository to our workstation. Then, we'll install `pipenv` and create a Python 3 virtualenv for this project.

```bash
$ git clone https://github.com/dennislwm/pgbackup
$ cd pgbackup
$ pip3.6 install --user pipenv
$ pipenv --python $(which python3.6)
```

To activate our new virtualenv, we use the command `pipenv shell`, and to deactivate it we use `exit`.

---
## Project Structure
     pgbackup/                        <-- Root of your project
       |- .gitignore                  <-- GitHub ignore 
       |- Makefile                    <-- Make 
       |- Pipfile                     <-- Pipenv 
       |- Pipfile.lock                <-- Pipenv lock 
       |- README.md                   <-- GitHub README markdown 
       |- README.rst                  <-- Python setuptools README 
       |- setup.cfg                   <-- Config file to create distribution wheel
       |- setup.py                    <-- Python script to create installable package
       +- bin/                        <-- Holds any bash scripts
          |- db_setup.sh              <-- CentOS 7 script to create and run our database
       +- data/                       <-- Sample output
       +- src/
          +- pgbackup/                <-- Holds any business logic
             |- __init__.py
             |- cli.py                <-- Python module to parse command line
             |- pgdump.py             <-- Python module to interface with pg_dump tool
             |- storage.py            <-- Python module to implement drivers
       +- tests/                      <-- Holds any automated tests
          |- test_cli.py              <-- Python script to test cli.py
          |- test_pgdump.py
          |- test_storage.py
---
## Test Driven Development

For this project, we're using `pytest` as our testing framework. We wrote a line in our `Makefile` that utilizes the `pytest`.

The file `test_cli.py` ensures that our ArgumentParser works as expected.

### Mocking in Test

We need to write tests that can run without an actual Postgres server running. FOr this, we will need to "stub" our interaction with `pg_dump` tool that comes with Postgres client that we installed.

Before we can use mocking in our tests, we need to install the `pytest-mock` package. This provides us with a `mocker` fixture that we can inject into our tests.

We're going to use `subprocess.Popen` instead of `.run` as we want the code to continue running instead of waiting for the subprocess to end. We're going to use `mocker.patch` on the `subprocess.Popen` in order to replace a different implementation that can be used for our testing.

The `mocker.patch` function creates an object `subprocess.Popen` that contains a method assert_called_with(). We'll use this method to assert the arguments passed to `subprocess.Popen` are as expected.

The file `test_pgdump.py` ensures that our code runs the proper third-party utility, i.e. `pg_dump`.

### Storage

The file `test_storage.py` ensures that our strategy for storing locally and on AWS S3 works as expected.

## Usage

### Workstation

Before we can use `pgbackup` in our workstation, we need to activate virtualenv and install our package locally.

*Note: You'll need to substitute in your database values for [USERNAME], [PASSWORD] and [SERVER_IP].*

```bash
$ pipenv shell
(pgbackup) $ pip install -e .
(pgbackup) $ pgbackup --driver local ./local-dump.sql postgres://[USERNAME]:[PASSWORD]@[SERVER_IP]:80/sample
```

To uninstall our package.

```bash
(pgbackup) $ pip uninstall pgbackup
```

### Production

We need to install using `pip install pgbackup` and then we can run the command `pgbackup --help`.

```bash
usage:
    Back up a PostgreSQL database locally or to AWS S3.

       [-h] --driver DRIVER DESTINATION [--schema] url

positional arguments:
  url                   URL of database to backup

optional arguments:
  -h, --help            show this help message and exit
  --driver DRIVER DESTINATION, -d DRIVER DESTINATION
                        how & where to store backup
  --schema, -s          Dump only the object definitions (schema), not data.
```

## Packaging

We can make our project create a console script for us when a user runs `pip install`. To do this, we need to add an entry point in our `setup.py`:

```python
    entry_points={
        'console_scripts': [
            'pgbackup=pgbackup.cli:main',
        ]
    },
```

Notice that we're referencing our `cli` module with a `:` and a `main`.

### Generating a Wheel

Before we can generate our `wheel`, we want to configure `setuptools` to not build the wheel for Python 2. We'll put this configuration in a `setup.cfg`.

```
[bdist_wheel]
python-tag = py36
```

We can run the following commands to build and install our wheel locally:

```bash
(pgbackup) $ python setup.py bdist_wheel
(pgbackup) $ pip install dist/pg-backup-0.1.0-py36-none-any.whl
```

We can also install from a remote source over HTTP, just use a public URL of the `whl` file with `pip install` instead of a local path.