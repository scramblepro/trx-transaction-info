from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .utils import get_tron_client, parse_basic_transfer


class TronTxView(APIView):
    def get(self, request, txid: str):
        cache_key = f"tron-tx:{txid}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        client = get_tron_client()
        try:
            tx = client.get_transaction(txid)
            info = client.get_transaction_info(txid)
        except Exception as e:
            return Response(
                {"error": "backend_error", "detail": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        result = {
            "txid": txid,
            "confirmed": bool(info),
            "block_number": info.get("blockNumber"),
            "block_time": info.get("blockTimeStamp"),
            "fee_sun": (
                info.get("fee", 0)
                or info.get("receipt", {}).get("net_fee", 0)
                or 0
            ),
            "fee_trx": (
                info.get("fee", 0)
                or info.get("receipt", {}).get("net_fee", 0)
                or 0
            ) / 1_000_000,
            "ret": info.get("receipt", {}).get("result"),
            "contract_result": info.get("contractResult"),
            "logs": info.get("log", []),
        }

        basic = parse_basic_transfer(tx)
        if basic:
            result.update({"transfer": basic})

        cache.set(cache_key, result, timeout=60)
        return Response(result)
