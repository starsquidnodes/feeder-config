#!/bin/bash

./scripts/create-feeder-config.py yaml/global.yml > toml/global.toml
./scripts/create-feeder-config.py yaml/north-america.yml > toml/north-america.toml
./scripts/create-feeder-config.py -x mexc yaml/global.yml > toml/global-nomexc.toml
./scripts/create-feeder-config.py -x mexc yaml/north-america.yml > toml/north-america-nomexc.toml