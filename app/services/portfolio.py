import json
import os
from rich.table import Table

class Portfolio:
    def __init__(self, storage_path="portfolio.json"):
        self.path = storage_path
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return {"positions": []}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def add(self, symbol, qty, price, fiat="BRL"):
        self.data["positions"].append({"symbol": symbol, "qty": qty, "price": price, "fiat": fiat})
        self._save()

    def table(self):
        t = Table(title="Posições")
        t.add_column("Símbolo")
        t.add_column("Qtd")
        t.add_column("Preço médio (fiat)")
        for p in self.data["positions"]:
            t.add_row(p["symbol"], str(p["qty"]), f"{p['fiat']} {p['price']}")
        return t
