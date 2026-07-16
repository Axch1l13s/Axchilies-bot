import requests


def scan_token(contract):

    url = f"https://api.dexscreener.com/latest/dex/tokens/{contract}"

    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        return None

    data = r.json()

    if not data.get("pairs"):
        return None

    pair = data["pairs"][0]

    return {
    "name": pair["baseToken"]["name"],
    "symbol": pair["baseToken"]["symbol"],
    "price": pair.get("priceUsd", "N/A"),
    "liquidity": pair["liquidity"]["usd"],
    "volume": pair["volume"]["h24"],
    "marketcap": pair.get("marketCap", 0),
    "dex": pair["dexId"],
    "chain": pair["chainId"],
    "url": pair["url"]
}