#!/usr/bin/env python3

import argparse
import json
import yaml


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("--no-urlsets", action="store_true")
    return parser.parse_args()


def header(title):
    return [
        "",
        "#",
        f"#  {title}".upper(),
        f"# {'-'*60}"
    ]


def main():
    args = parse_args()

    config = yaml.safe_load(open(args.filename, "r"))

    lines = header("currency pairs")[1:]

    old_base = ""
    for cp_name, cp_config in config.get("currency_pairs", {}).items():
        base, quote = cp_name.split("-")

        if old_base != "" and base != old_base:
            weights = config.get("provider_weights", {}).get(old_base)
            if weights:
                lines += [
                    '',
                    f'[provider_weight.{old_base}]'
                ]
                for provider, weight in weights.items():
                    lines += [
                        f'{provider} = {weight}'
                    ]

        providers = [x.strip() for x in cp_config["providers"].split(",")]
        twap = cp_config.get("twap")
        lines += [
            '',
            '[[currency_pairs]]',
            f'base = "{base}"',
            f'quote = "{quote}"',
            f'providers = {json.dumps(sorted(providers))}'
        ]

        if twap:
            lines += [
                'derivative = "twap"',
                f'derivative_period = "{twap}"'
            ]

        old_base = base

    lines += header("provider overrides")

    min_providers = {}
    for mp_denom, mp_value in config.get("min_providers", {}).items():
        if mp_value not in min_providers.keys():
            min_providers[mp_value] = []
        min_providers[mp_value].append(mp_denom)

    for mp_value, mp_denoms in min_providers.items():
        lines += [
            '',
            '[[provider_min_overrides]]',
            f'denoms = {json.dumps(sorted(mp_denoms))}',
            f'providers = {mp_value}'
        ]

    lines += header("deviation thresholds")

    for dt_base, dt_value in config.get("deviation_thresholds", {}).items():
        lines += [
            '',
            '[[deviation_thresholds]]',
            f'base = "{dt_base}"',
            f'threshold = "{dt_value}"'
        ]

    if not args.no_urlsets:
        lines += header("url sets")

        for us_name, us_urls in config.get("url_sets").items():
            lines += [
                '',
                f'[url_set.{us_name}]',
                f'urls = ['
            ]
            for url in us_urls:
                lines += [f'  "{url}",']
            lines += [']']

    lines += header("endpoints")

    for ep_name, ep_config in config.get("endpoints").items():
        lines += [
            '',
            '[[provider_endpoints]]',
            f'name = "{ep_name}"'
        ]

        urls = ep_config.get("urls", [])
        if urls:
            lines += ['urls = [']
            for url in urls:
                lines += [f'  "{url}",']
            lines += [']']

        url_set = ep_config.get("url_set", None)
        if url_set:
            lines += [f'url_set = "{url_set}"']

    for c_provider, c_addresses in config.get("contracts", {}).items():
        lines += [
            '',
            f'[contract_addresses.{c_provider}]'
        ]
        for symbol, address in c_addresses.items():
            lines += [f'{symbol} = "{address}"']

    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
