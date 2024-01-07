#!/usr/bin/env python3
import sys
import requests
import yaml

def get_pairs_binance(endpoint):
    info_res = requests.get(f"{endpoint}/api/v3/exchangeInfo")
    info_res.raise_for_status()
    return [f"{s['baseAsset']}-{s['quoteAsset']}" for s in info_res.json()["symbols"]]

def get_pairs(provider):
    if provider == "binance":
        return get_pairs_binance("https://api.binance.com")
    elif provider == "binanceus":
        return get_pairs_binance("https://api.binance.us")
    else:
        raise RuntimeError("provider not supported")

def extend_yaml_config(provider, symbols, config_data):
    config_symbols = config_data["currency_pairs"]
    for symbol, data in config_symbols.items():
        providers = data["providers"]
        if symbol in symbols:
            providers_list = providers.split(",")
            if provider not in providers_list:
                providers_list.append(provider)
                config_data["currency_pairs"][symbol]["providers"] = ", ".join(providers_list)

def remove_yaml_config(provider, config_data):
    config_symbols = config_data["currency_pairs"]
    for symbol, data in config_symbols.items():
        providers = data["providers"]
        providers_list = [p.strip() for p in providers.split(",")]
        if provider in providers_list:
            providers_list.remove(provider)
            config_data["currency_pairs"][symbol]["providers"] = ", ".join(providers_list)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: get-pairs.py <provider> [yaml_config]")
        print("\toutputs pairs supported by provider.")
        print("\tif yaml config is provided, outputs a modified config with the provider added to supported pairs.")
        print("\tprefix the provider name with a dash to remove it from all pairs in the config where it exists.")
        sys.exit(-1)
    provider = sys.argv[1]
    is_negated = provider.startswith("-")
    if is_negated:
        provider = provider[1:]
    if len(sys.argv) == 2:
        if is_negated:
            raise RuntimeError("negation not supported with one argument")
        print(get_pairs(provider))
    elif len(sys.argv) > 2:
        with open(sys.argv[2], "rb") as f:
            config_data = yaml.safe_load(f)
        if is_negated:
            remove_yaml_config(provider, config_data)
        else:
            symbols = get_pairs(provider)
            extend_yaml_config(provider, symbols, config_data)
        print(yaml.safe_dump(config_data, width=float("inf")))