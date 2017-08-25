SHELL=C:/Windows/System32/cmd.exe
ENV = env
PYBIN = $(ENV)/scripts
PYTHON = $(PYBIN)/python
PIP = $(PYBIN)/pip
PYTEST = $(PYTHON) -m pytest
COVERAGE = $(PYTHON) -m coverage
PYFLAKE8 = $(PYTHON) -m flake8
TESTDIR = tests
MODULE_NAME = reqlog
DEV_CONFIG_FILE = ./conf/reqlog-dev.conf
NPM = npm
MKDIR = mkdir
TMP_PATH = .\tmp
CPDIR = xcopy
STATIC_FILES_DIR = .\static
CPDIR_KEYS = /e /i /h
BASE_DOCKER_IMAGE_TAG=reqlog_base

environ: clean requirements.txt requirements-dev.txt
	virtualenv $(ENV)
	$(PIP) install -r requirements-dev.txt
	$(MAKE) init_static
	@echo "initialization complete"

.PHONY: help
help:
	@echo "make                      # create virtual env and setup dependencies"
	@echo "make tests                # run tests"
	@echo "make coverage             # run tests with coverage report"
	@echo "make run                  # run server at localhost"
	@echo "make lint                 # check linting"
	@echo "make flake8               # alias for `make lint`"
	@echo "make clean                # remove more or less everything created by make"
	@echo "make redcw                # remove exited Docker containers (for Windows)"
	@echo "make idea_clean           # clean everything and prepare project to export"
	@echo "make export               # clean ABSOLUTELLY everything except code (even .git) and reinit db"
	@echo "make drop_database        # remove more or less everything created by make"
	@echo "make create_database      # create all tables in database"
	@echo "make init_database        # initialize database with initial data"
	@echo "make reinit_database      # drop tables, create new and init with initial data"
	@echo "make gen_test_requests    # generate test requests for Demo user"
	@echo "make gen_ksuid            # generate ksuid and write to console"
	@echo "make gen_ksuid62          # generate ksuid, encode as Base62 and write to console"
	@echo "make init_static          # initialize static files"
	@echo "make docker_base          # build docker base image"
	@echo "make docker_image         # build complete docker image"
	@echo "make run_docker_container # run built docker container (docker-compose)"
	@echo "make up_redis             # start Redis docker container locally (standalone)"

.PHONY: run
run:
	$(PYTHON) -m $(MODULE_NAME) --config $(DEV_CONFIG_FILE)

.PHONY: tests
tests:
	$(PYTEST) $(TESTDIR) -vv

.PHONY: coverage
coverage:
	$(PYTEST) $(TESTDIR) -vv --cov=$(MODULE_NAME)
	$(COVERAGE) html

.PHONY: create_db_folder
create_db_folder:
	@if not exist db mkdir db
	
.PHONY: drop_database	
drop_database:
	$(MAKE) create_db_folder
	$(PYTHON) -m $(MODULE_NAME).dbmgt --drop_database --config $(DEV_CONFIG_FILE)

.PHONY: create_database
create_database:
	$(MAKE) create_db_folder
	$(PYTHON) -m $(MODULE_NAME).dbmgt --create_database --config $(DEV_CONFIG_FILE)

.PHONY: init_database
init_database:
	$(MAKE) create_db_folder
	$(PYTHON) -m $(MODULE_NAME).dbmgt --init_database --config $(DEV_CONFIG_FILE)

.PHONY: reinit_database
reinit_database: drop_database create_database init_database

.PHONY: gen_test_events
gen_test_events:
	$(PYTHON) -m $(MODULE_NAME).dbmgt --gen_test_events --config $(DEV_CONFIG_FILE)

.PHONY: lint
lint:
	$(PYFLAKE8)
	
.PHONY: flake8
flake8:
	$(PYFLAKE8)

.PHONY: redcw
redcw:
	.\infrastructure\tools\win\redcw.bat

.PHONY: clean
clean:
	if exist $(ENV) rd $(ENV) /q /s
	if exist reqlog.egg-info rd reqlog.egg-info /q /s
	if exist .coverage del .coverage
	if exist htmlcov rd htmlcov /q /s
	if exist log rd log /q /s
	if exist $(TMP_PATH) rd $(TMP_PATH) /q /s
	if exist $(STATIC_FILES_DIR) rd $(STATIC_FILES_DIR) /q /s
	del /S *.pyc

.PHONY: idea_clean
idea_clean: clean
	if exist .cache rd .cache /q /s
	if exist .idea rd .idea /q /s
	
.PHONY: export
export: 
	if exist db rd db /q /s
	mkdir db
	$(MAKE) reinit_database
	$(MAKE) idea_clean
	if exist bp rd bp /q /s
	if exist logs rd logs /q /s	
	if exist .git rd .git /q /s

.PHONY: gen_ksuid
gen_ksuid:
	$(PYTHON) -m $(MODULE_NAME).utils.gen_ksuid

.PHONY: gen_ksuid62
gen_ksuid62:
	$(PYTHON) -m $(MODULE_NAME).utils.gen_ksuid --base62

.PHONY: init_static
init_static:
	if not exist $(TMP_PATH) $(MKDIR) $(TMP_PATH)
	if exist $(STATIC_FILES_DIR) rd $(STATIC_FILES_DIR) /q /s
	$(NPM) install admin-lte --prefix $(TMP_PATH)
	$(MKDIR) $(STATIC_FILES_DIR)
	$(CPDIR) $(TMP_PATH)\node_modules\admin-lte\bootstrap $(STATIC_FILES_DIR)\bootstrap $(CPDIR_KEYS)
	$(CPDIR) $(TMP_PATH)\node_modules\admin-lte\build $(STATIC_FILES_DIR)\build $(CPDIR_KEYS)	
	$(CPDIR) $(TMP_PATH)\node_modules\admin-lte\dist $(STATIC_FILES_DIR)\dist $(CPDIR_KEYS)
	$(CPDIR) $(TMP_PATH)\node_modules\admin-lte\plugins $(STATIC_FILES_DIR)\plugins $(CPDIR_KEYS)	
	$(CPDIR) $(MODULE_NAME)\data\imgs $(STATIC_FILES_DIR)\imgs $(CPDIR_KEYS)	
	
.PHONY: docker_base
docker_base:
	@docker build -t $(BASE_DOCKER_IMAGE_TAG) -f docker-base .
	
.PHONY: docker_image
docker_image:
	@docker-compose -f docker-compose.yml build

.PHONY: run_docker_container
run_docker_container:
	@docker-compose -f docker-compose.yml up

.PHONY: up_redis
up_redis:
	@docker run -d -p 6379:6379 --rm redis
