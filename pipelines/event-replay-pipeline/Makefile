SHELL := /bin/sh
PY_VERSION := 3.7

export PYTHONUNBUFFERED := 1

SRC_DIR := src
SAM_DIR := .aws-sam

# Required environment variables (user must override)

# S3 bucket used for packaging SAM templates
PACKAGE_BUCKET ?= your-bucket-here

# user can optionally override the following by setting environment variables with the same names before running make

# Path to system pip
PIP ?= pip
# Default AWS CLI region
AWS_DEFAULT_REGION ?= us-east-1

PYTHON := $(shell /usr/bin/which python$(PY_VERSION))

.DEFAULT_GOAL := build

clean:
	rm -f $(SRC_DIR)/requirements.txt
	rm -rf $(SAM_DIR)

# used once just after project creation to lock and install dependencies
bootstrap:
	$(PYTHON) -m $(PIP) install pipenv --user
	pipenv lock
	pipenv sync --dev

# used by CI build to install dependencies
init:
	$(PYTHON) -m $(PIP) install pipenv --user
	pipenv sync --dev

compile:
	pipenv run flake8 src
	pipenv run pydocstyle src
	pipenv run cfn-lint template.yml
	pipenv run py.test --cov=src --cov-fail-under=85 -vv test/unit
	pipenv lock --requirements > $(SRC_DIR)/requirements.txt
	pipenv run sam build

build: compile

package: compile
	pipenv run sam package --s3-bucket $(PACKAGE_BUCKET) --output-template-file $(SAM_DIR)/packaged-template.yml

publish: package
	pipenv run sam publish --template $(SAM_DIR)/packaged-template.yml
