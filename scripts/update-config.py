#!/usr/bin/env python3

import argparse
import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", type=str, default="master")
    parser.add_argument("--custom", type=str, required=True)
    parser.add_argument("--config", type=str, default="global")

    return parser.parse_args()


def main():
    args = parse_args()

    path = f"starsquid/feeder-config/{args.tag}/toml/{args.config}"
    response = requests.get(f"https://raw.githubusercontent.com/{path}")

    if response.status_code != 200:
        return

    print(response.text)

    config = ""
    if args.custom:
        config = open(args.custom, "r").read() + "\n"

    print(config + response.text)


if __name__ == "__main__":
    main()
