import os
from functools import lru_cache
from tronpy import Tron
from tronpy.providers import HTTPProvider


@lru_cache(maxsize=1)
def get_tron_client():
    network = os.getenv("TRON_NETWORK", "mainnet")
    fullnode = os.getenv("TRON_FULLNODE_URL") or None
    solidity = os.getenv("TRON_SOLIDITYNODE_URL") or None

    if fullnode or solidity:
        providers = {}
        if fullnode:
            providers["full_node"] = HTTPProvider(fullnode)
        if solidity:
            providers["solidity_node"] = HTTPProvider(solidity)
        return Tron(network=network, **providers)

    return Tron(network=network)




def parse_basic_transfer(tx):
    """Если это TransferContract (обычный TRX перевод) — достаём from/to/amount."""
    try:
        c = tx["raw_data"]["contract"][0]
        ctype = c["type"]
        if ctype != "TransferContract":
            return None
        p = c["parameter"]["value"]
        owner = p.get("owner_address")
        to = p.get("to_address")
        amount_sun = int(p.get("amount", 0))
        return {
            "contract_type": ctype,
            "from": owner,
            "to": to,
            "amount_sun": amount_sun,
            "amount_trx": amount_sun / 1_000_000,
        }
    except Exception:
        return None