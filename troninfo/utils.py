from tronpy import Tron
from tronpy.providers import HTTPProvider
import os


def get_tron_client():
    """Возвращает клиент Tron, использующий TRON_API_KEY если он есть.
    
    Используется lru_cache, чтобы повторно не создавать клиента и не
    переподключаться при каждом HTTP-запросе.
    """
    api_key = os.getenv("TRON_API_KEY")
    if not api_key:
        raise RuntimeError("TRON_API_KEY not set in environment")

    return Tron(HTTPProvider(api_key=api_key))



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
