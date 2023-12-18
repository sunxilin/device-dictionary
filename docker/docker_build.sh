#!/bin/bash

docker build -t device_dictionary:"$1" -f docker/Dockerfile .