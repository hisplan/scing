#!/usr/bin/env bash

CROMWELL_VERSION="59"

mkdir -p devtools

curl -L -o devtools/cromwell-${CROMWELL_VERSION}.jar https://github.com/broadinstitute/cromwell/releases/download/${CROMWELL_VERSION}/cromwell-${CROMWELL_VERSION}.jar
curl -L -o devtools/womtool-${CROMWELL_VERSION}.jar https://github.com/broadinstitute/cromwell/releases/download/${CROMWELL_VERSION}/womtool-${CROMWELL_VERSION}.jar

# cd devtools
ln -snf cromwell-${CROMWELL_VERSION}.jar cromwell.jar
ln -snf womtool-${CROMWELL_VERSION}.jar womtool.jar
