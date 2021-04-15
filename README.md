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

<!-- /TOC -->

## Project

Create a CLI tool that we can use to easily back up a PostgreSQL database to either AWS S3 or locally. The parameters are:

1. Database URL to backup
2. Driver (either `local` or `S3`)
3. Backup destination (a file path for `local` or a bucket name for `S3`)

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
$ wget https://download.postgresql.org/pub/repos/yum/9.6/redhat/
rhel-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
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
$ git clone https://github.com/dennislwm/pgbackup .
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
       |- setup.py                    <-- Python script to create installable package
       +- bin/                        <-- Holds any bash scripts
          |- db_setup.sh              <-- CentOS 7 script to create and run our database
       +- src/
          +- pgbackup/                <-- Holds any business logic
             |- __init__.py
             |- cli.py                <-- Python script to parse command line
       +- tests/                      <-- Holds any automated tests
          |- test_cli.py              <-- Python script to test CLI
