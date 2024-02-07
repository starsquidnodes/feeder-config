#!/bin/bash

./scripts/create-feeder-config.py -x mexc yaml/global.yml > toml/global.toml
./scripts/create-feeder-config.py -x mexc yaml/north-america.yml > toml/north-america.toml