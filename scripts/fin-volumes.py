#!/usr/bin/env python3

import argparse
import requests


def parse_args():
    parser = argparse.ArgumentParser()
    return parser.parse_args()


def main():
    args = parse_args()

    response = requests.get("https://api.kujira.app/api/coingecko/tickers")
    if response.status_code != 200:
        return

    data = response.json()
    volumes = {}

    for ticker in data.get("tickers", []):
        base = ticker["base_currency"]
        quote = ticker["target_currency"]
        volume = float(ticker["base_volume"])
        if base not in volumes.keys():
            volumes[base] = {}
        volumes[base][quote] = volume

    for base, quotes in volumes.items():
        quotes = dict(
            sorted(quotes.items(), key=lambda item: item[1], reverse=True))
        for quote, volume in quotes.items():
            print(base, quote, volume)


if __name__ == "__main__":
    main()
