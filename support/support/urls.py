import json
import time

import requests
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

cache = {}


@csrf_exempt
def get_current_market_state(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            currency_from = data.get("currency_from")
            currency_to = data.get("currency_to")

            if not currency_from or not currency_to:
                raise Exception("Currency from and currency to are required.")

            cached_response = cache.get(currency_from, {}).get(currency_to)
            if cached_response is not None:
                if time.time() - cached_response["timestamp"] < 10:
                    return JsonResponse(
                        {
                            "exchange_rate": cached_response["value"],
                            "cached": True,
                        }
                    )

            api_key = "WC91R1D8QFCGIZN9"
            url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency_from}&to_currency={currency_to}&apikey={api_key}"

            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            exchange_rate_data = data.get("Realtime Currency Exchange Rate")
            if exchange_rate_data is None:
                raise Exception(
                    "Key 'Realtime Currency Exchange Rate' "
                    "not found in API response."
                )

            rate = exchange_rate_data.get("5. Exchange Rate")

            if currency_from not in cache:
                cache[currency_from] = {}
            cache[currency_from][currency_to] = {
                "value": rate,
                "timestamp": time.time(),
            }
            return JsonResponse({"exchange_rate": rate, "cached": False})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)


urlpatterns = [
    path("exchange_rate/", get_current_market_state),
]
