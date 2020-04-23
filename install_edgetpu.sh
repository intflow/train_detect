#!/bin/bash

# Install the compiler:
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list
apt-get update
apt-get install edgetpu-compiler
