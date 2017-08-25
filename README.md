# reqlog

General purpose Web-application for events gathering.

Can be useful for IoT devices events gathering with authentication using tokens. Gathered events can be acessed via web interface or RESTful JSON API.

## Technologies and utilities

### Core

This project uses these core technologies and tools.

* `Python 3` and and [Bottle](https://bottlepy.org/docs/dev/) web-framework.
* [JWT](https://jwt.io/) for authentication and authorization.
* `make` for actions management;

### Code management
* [Flake8](http://flake8.pycqa.org/en/latest/) as linter.

### Testing

* [pytests](https://docs.pytest.org/en/latest/) for unittesting 
* [mock](https://pypi.python.org/pypi/mock) and [requests-mock](https://pypi.python.org/pypi/requests-mock) for mocking;
* [webtests](https://pypi.python.org/pypi/WebTest) for functional testing;
* [coverage](https://coverage.readthedocs.io/en/) for tests coverage calculation.


## Pre-install

First of all you should have `Python 3` and `pip` installed. Also you need:

* `virtualenv`
* `make`
* `Docker`
* `npm`

For Windows users:

* you can install `virtualenv` using `pip install virtualenv`;
* make for Windows can be found [here](http://gnuwin32.sourceforge.net/packages/make.htm)
* Docker can be found [here](https://www.docker.com/docker-windows)
* npm can found [here](https://www.npmjs.com/package/npm)

Next you should go to project directory and just run `make` This will install all needful utilities, tools and setup working directory.

Note: you can use `make help` to see all available commands and functions.

## Deploy

This web-application can be deployed into AWS or bare-metal server.

I preferr to use `nginx + uwsgi + supervisord` in `Docker`. You can build Docker container for further deployment. More information can be found in `Docker` section of this document.

## Make commands

Makefile support these commands:

* `make help` - list all available commands;
* `make` - create virtual env and setup dependencies;
* `make tests` - run tests;
* `make coverage` - run tests with coverage report;
* `make lint` - check linting;
* `make flake8` - alias for `make lint`;
* `make clean` - remove more or less everything created by make.
* `make run` - run server at localhost;
* `make drop_database` - remove more or less everything created by make
* `make create_database` - create all tables in database
* `make init_database` - initialize database with initial data
* `make reinit_database` - drop tables, create new and init with initial data;

Experimental commands (can removed in future):

* `make redcw` - remove exited Docker containers (for Windows);
* `make idea_clean` - clean everything and prepare project to export;
* `make export` - clean ABSOLUTELLY everything except code (even .git) and reinit db;
* `make gen_test_requests` - generate test requests for Demo user;
* `make gen_ksuid` - generate ksuid and write to console;
* `make gen_ksuid62` - generate ksuid, encode as Base62 and write to console;
* `make init_static` - initialize static files;

Docker support (not implemented now, only some features in some branches):

* `make docker_base` - build docker base image;
* `make docker_image` - build complete docker image;
* `make run_docker_image` - run built docker container;
* `make up_redis` - start Redis docker container locally.


## Check running

To check running instance (for example, initialized by `make run`) you can go to http://localhost:9000/version using your browser. If everything is OK you will receive something like this:

```JSON
{
    "app_name":"reqlog",
    "version":"0.1.0.0"
}
```

Also, you can log to UI by going to http://localhost:9000/version with login `demo@gmail.com` and password `demo`.


## Docker

`reqlog` can be build as Docker image for further deployment on server. 

To build under Windows you just need execute:

* `make docker_base` - will build base image based on Debian and required utilities and servers;
* `make docker_image` - will build image with reqlog and SQLite database;


If you want build using command line you should execute (in root folder):

* `docker build -t reqlog_base -f docker-base .` to build base image;
* `docker build -t reqlog_container --build-arg application=reqlog --build-arg DOCKER_BASE=docker-base -f docker .`  to build image with `reqlog` installed.

**Warn:** please note that command lines contains dot ("`.`" symbol at end).

To run built Docker containers you should run:

`docker run --rm -d -p 80:9000 -v ./logs:/var/log/supervisor reqlog_container`

This will start built container that will be accessible at port 9000. You can check that everything is OK just by visiting http://localhost:9000/version If everything is OK, you will get something like this:

```json
{
    "app_name":"reqlog",
    "version":"0.1.0.0"
}
```

If you want log into system, you can go to http://localhost:9000 with login `demo@gmail.com` and password `demo`

Hope you like it. Enjoy!