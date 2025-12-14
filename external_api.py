import requests
from flask import Blueprint, jsonify, request

external_api_bp = Blueprint("external_api", __name__)

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"


class ExternalAPIError(Exception):
    """Custom exception for external API failures."""
    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.status_code = status_code


def fetch_external_coin_data(endpoint: str, params: dict | None = None):
    """
    Generic helper to call CoinGecko API.
    """
    url = f"{COINGECKO_BASE_URL}{endpoint}"
    try:
        resp = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        raise ExternalAPIError(f"Error connecting to external crypto API: {e}", status_code=503)

    if not resp.ok:

        if resp.status_code == 404:
            raise ExternalAPIError("Coin not found in external API", status_code=404)
        raise ExternalAPIError(
            f"External crypto API returned status {resp.status_code}",
            status_code=502
        )

    try:
        data = resp.json()
    except ValueError:
        # Malformed JSON
        raise ExternalAPIError("External crypto API returned invalid JSON", status_code=502)

    return data


@external_api_bp.route("/coins/live-prices", methods=["GET"])
def get_live_prices():
    """
    Get live prices for one or more coins from CoinGecko.

    Query params:
      - ids: comma-separated coin IDs (default: 'bitcoin')
      - vs_currencies: comma-separated currencies (default: 'usd')
    """
    coin_ids = request.args.get("ids", "bitcoin")
    vs_currencies = request.args.get("vs_currencies", "usd")

    if not coin_ids.strip():
        return jsonify({"error": "ids parameter is required"}), 400

    params = {
        "ids": coin_ids,
        "vs_currencies": vs_currencies
    }

    try:
        data = fetch_external_coin_data("/simple/price", params=params)
    except ExternalAPIError as e:
        return jsonify({"error": str(e)}), e.status_code

    return jsonify({
        "source": "coingecko",
        "ids": coin_ids.split(","),
        "vs_currencies": vs_currencies.split(","),
        "data": data
    }), 200


@external_api_bp.route("/coins/<coin_id>/external-info", methods=["GET"])
def get_coin_external_info(coin_id):
    """
    Get detailed metadata and market info for a single coin.
    """
    if not coin_id:
        return jsonify({"error": "coin_id is required"}), 400

    params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true",
        "community_data": "false",
        "developer_data": "false",
        "sparkline": "false",
    }

    try:
        data = fetch_external_coin_data(f"/coins/{coin_id}", params=params)
    except ExternalAPIError as e:
        return jsonify({"error": str(e)}), e.status_code

    normalized = {
        "id": data.get("id"),
        "symbol": data.get("symbol"),
        "name": data.get("name"),
        "image": data.get("image", {}).get("large"),
        "current_price_usd": data.get("market_data", {})
                              .get("current_price", {})
                              .get("usd"),
        "market_cap_usd": data.get("market_data", {})
                            .get("market_cap", {})
                            .get("usd"),
        "price_change_24h": data.get("market_data", {})
                               .get("price_change_percentage_24h"),
        "homepage": (data.get("links", {}) or {})
                    .get("homepage", [None])[0],
    }

    return jsonify({
        "source": "coingecko",
        "data": normalized
    }), 200

