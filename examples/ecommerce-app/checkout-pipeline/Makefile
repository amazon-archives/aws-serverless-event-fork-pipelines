SHELL := /bin/sh
PY_VERSION := 3.6

export PYTHONUNBUFFERED := 1

BUILD_DIR := dist

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
	rm -rf $(BUILD_DIR)

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
	mkdir -p $(BUILD_DIR)
	pipenv run flake8 src
	pipenv run pydocstyle src
	pipenv run cfn-lint template.yml
	pipenv run py.test --cov=src --cov-fail-under=85 -vv test/unit

build: compile

package: compile
	cp -r template.yml src $(BUILD_DIR)

	# package dependencies in lib dir
	pipenv lock --requirements > $(BUILD_DIR)/requirements.txt
	pipenv run pip install -t $(BUILD_DIR)/src/lib -r $(BUILD_DIR)/requirements.txt

	# replace code local references with S3
	pipenv run sam package --template-file $(BUILD_DIR)/template.yml --s3-bucket $(PACKAGE_BUCKET) --output-template-file $(BUILD_DIR)/packaged-template.yml
