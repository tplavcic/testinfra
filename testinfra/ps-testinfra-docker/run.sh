#!/usr/bin/env bash
export PS_VERSION="8.0.20-11.3"
export PS_REVISION="5b5a5d2"
export DOCKER_ACC="percona"
pytest -v --junit-xml report.xml $@
