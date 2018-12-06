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

init:
	$(PYTHON) -m $(PIP) install pipenv --user
	pipenv sync --dev

compile:
	mkdir -p $(BUILD_DIR)
	pipenv run flake8 app
	pipenv run pydocstyle app
	pipenv run cfn-lint template.yml

build: compile

package: compile
	cp -r template.yml app $(BUILD_DIR)

	# package dependencies in lib dir
	pipenv lock --requirements > $(BUILD_DIR)/requirements.txt
	pipenv run pip install -t $(BUILD_DIR)/app/lib -r $(BUILD_DIR)/requirements.txt

	# replace code local references with S3
	pipenv run sam package --template-file $(BUILD_DIR)/template.yml --s3-bucket $(PACKAGE_BUCKET) --output-template-file $(BUILD_DIR)/packaged-app.yml
