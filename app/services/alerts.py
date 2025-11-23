import json
import os
import time
from datetime import datetime
import httpx

API_SIMPLE = "https://api.coingecko.com/api/v3/simple/price"

class AlertManager:
    def __init__(self, storage_path="alerts.json"):
        self.path = storage_path
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return {"alerts": []}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def add(self, symbol, target, kind="price"):
        self.data["alerts"].append({
            "symbol": symbol,
            "target": target,
            "kind": kind,
            "created_at": datetime.utcnow().isoformat()
        })
        self._save()

def beta_watch_3pct(symbol: str, fiat: str = "brl", refresh_seconds: int = 20, console=None):
    """
    Observa variações e dispara alerta a cada ±3% em relação ao último marco.
    Beta: fixo em 3%; Pro: configurável (fora desta função).
    """
    with httpx.Client(timeout=10) as client:
        # preço inicial
        r = client.get(API_SIMPLE, params={"ids": symbol, "vs_currencies": fiat})
        r.raise_for_status()
        base_price = float(r.json().get(symbol, {}).get(fiat, 0))
        if console:
            console.print(f"[cyan]Preço base[/cyan]: {symbol.upper()} {fiat.upper()} {base_price:.4f}")

        last_mark = base_price
        while True:
            time.sleep(refresh_seconds)
            r = client.get(API_SIMPLE, params={"ids": symbol, "vs_currencies": fiat})
            r.raise_for_status()
            price = float(r.json().get(symbol, {}).get(fiat, 0))
            change_pct = ((price - last_mark) / last_mark) * 100 if last_mark else 0.0

            if change_pct >= 3.0:
                if console:
                    console.print(f"[green]↗ Alta +{change_pct:.2f}%[/green] — Novo marco: {price:.4f}")
                last_mark = price
            elif change_pct <= -3.0:
                if console:
                    console.print(f"[red]↘ Queda {change_pct:.2f}%[/red] — Novo marco: {price:.4f}")
                last_mark = price
            else:
                if console:
                    console.print(f"[white]Δ {change_pct:.2f}%[/white] — Preço: {price:.4f}")
