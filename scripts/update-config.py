#!/usr/bin/env python3

import argparse
import requests

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", type=str, default="master")
    parser.add_argument("--custom", type=str, required=True)
    parser.add_argument("--config", type=str, default="global")
    parser.add_argument("--us-feeder", action="store_true")  # Add this line for --us-feeder

    return parser.parse_args()

def main():
    args = parse_args()

    path = f"starsquidnodes/feeder-config/{args.tag}/toml/{args.config}.toml"
    response = requests.get(f"https://raw.githubusercontent.com/{path}")

    if response.status_code != 200:
        return

    config = open(args.custom, "r").read() + "\n"
    combined_config = config + response.text

    if args.us_feeder:  # Check if --us-feeder is set
        combined_config = combined_config.replace('"binance"', '"binanceus"')

    print(combined_config)

if __name__ == "__main__":
    main()
