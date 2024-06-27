#!/bin/bash

for i in global north-america testnet; do
    ./scripts/create-feeder-config.py -x mexc yaml/$i.yml > toml/$i.toml
done