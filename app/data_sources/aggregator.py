import httpx

API_MARKETS = "https://api.coingecko.com/api/v3/coins/markets"
API_CHART = "https://api.coingecko.com/api/v3/coins/{id}/market_chart"

def get_market_snapshot(limit: int = 20, fiat: str = "brl"):
    params = {
        "vs_currency": fiat.lower(),
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "24h,7d"
    }
    with httpx.Client(timeout=10) as client:
        r = client.get(API_MARKETS, params=params)
        r.raise_for_status()
        items = r.json()
    data = []
    for i, it in enumerate(items, start=1):
        data.append({
            "rank": i,
            "symbol": it.get("symbol", "").upper(),
            "price": float(it.get("current_price", 0)),
            "change_24h": float(it.get("price_change_percentage_24h_in_currency", 0) or 0),
            "change_7d": float(it.get("price_change_percentage_7d_in_currency", 0) or 0),
            "volume_24h": float(it.get("total_volume", 0)),
            "market_cap": float(it.get("market_cap", 0)),
        })
    return data

def get_price_history(symbol_id: str, fiat: str = "brl", days: int = 7, interval: str = "hourly"):
    # symbol_id deve ser o 'id' do CoinGecko (ex.: 'bitcoin', 'ethereum')
    params = {"vs_currency": fiat.lower(), "days": days, "interval": interval}
    with httpx.Client(timeout=10) as client:
        r = client.get(API_CHART.format(id=symbol_id), params=params)
        r.raise_for_status()
        js = r.json()
    prices = js.get("prices", [])
    # Converter timestamps para índices simples para o terminal
    times = list(range(1, len(prices) + 1))
    values = [float(p[1]) for p in prices]
    return times, values
