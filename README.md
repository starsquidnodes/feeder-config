# feeder-config

Unofficial configurations, scripts and examples for [Kujira price feeder](https://github.com/Team-Kujira/oracle-price-feeder)

## Simple update

Create a toml that holds your price feeder specific settings as well as your custom url sets

```toml
gas_adjustment = 2.5
gas_prices = "0.0034ukuji"
enable_server = true
enable_voter = true
provider_timeout = "1s"

history_db = "/var/tmp/feeder.db"

[server]
listen_addr = "0.0.0.0:7171"
read_timeout = "20s"
verbose_cors = true
write_timeout = "20s"

[account]
address = "kujira1..."
chain_id = "kaiyo-1"
validator = "kujiravaloper..."
prefix = "kujira"
# fee_granter = "kujira..."

[keyring]
backend = "file"
dir = "/home/kujira-feeder"

[rpc]
grpc_endpoint = "localhost:9090"
rpc_timeout = "100ms"
tmrpc_endpoint = "http://localhost:26657"

[telemetry]
enable_hostname = true
enable_hostname_label = true
enable_service_label = true
enabled = true
global_labels = [["chain_id", "kaiyo-1"]]
service_name = "price-feeder"
type = "prometheus"
# prometheus_retention = 120

#
#  URL SETS
# ------------------------------------------------------------

[url_set.fin]
urls = ["https://kaiyo-1.gigalixirapp.com"]

[url_set.api_kujira]
urls = [
  "http://127.0.0.1:11702",
  "https://api-kujira.starsquid.io"
]
```

Update your feeder config

```sh
update-config.py --tag v1.0.0 --custom custom.toml --config global > config.toml
```

## Configs

### `global`

This config makes use of (almost) all available price sources including `binance` and `binanceus`

Required URL sets:

```toml
# providers: finv2
# https://cosmos.directory/kujira/nodes (REST)
[url_set.api_kujira]
urls = []

# providers: astroport_neutron
# https://cosmos.directory/neutron/nodes (REST)
[url_set.api_neutron]
urls = []

# providers: osmosisv2
# https://cosmos.directory/osmosis/nodes (REST)
[url_set.api_osmosis]
urls = []

# providers: uniswapv3
# https://ethereumnodes.com
[url_set.rpc_ethereum]
urls = []

# providers: fin
# ["https://api.kujira.app", "https://kaiyo-1.gigalixirapp.com"]
[url_set.fin]
urls = []
```

## YAML to TOML converter

To make config maintenance a bit easier, you can define the price source config in YAML notation and convert it to TOML with

```sh
create-feeder-config.py your-config.yml
```
