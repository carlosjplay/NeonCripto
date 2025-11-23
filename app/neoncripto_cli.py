import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from dotenv import load_dotenv
import os
import time

from app.services.beta_gate import is_pro
from app.services.ai_assistant import ask_ai
from app.data_sources.aggregator import get_market_snapshot, get_price_history
from app.services.portfolio import Portfolio
from app.services.alerts import AlertManager, beta_watch_3pct
from app.ui.charts import plot_line

app = typer.Typer(help="NEONCRIPTO - Criptomoedas ao vivo com gráficos e alertas.")
console = Console()
load_dotenv()

portfolio = Portfolio(storage_path=os.getenv("PORTFOLIO_PATH", "portfolio.json"))
alerts = AlertManager(storage_path=os.getenv("ALERTS_PATH", "alerts.json"))

@app.command()
def dashboard(top: int = 20, fiat: str = "BRL"):
    """Mostra o dashboard com os principais ativos."""
    console.rule("[bold magenta]NEONCRIPTO - Dashboard")
    data = get_market_snapshot(limit=top, fiat=fiat)
    table = Table(title=f"Top {top} - Cotação em {fiat}", show_lines=False)
    table.add_column("Rank", justify="right")
    table.add_column("Símbolo")
    table.add_column("Preço")
    table.add_column("24h")
    table.add_column("7d")
    table.add_column("Volume 24h")
    table.add_column("Market Cap")

    for row in data:
        c24 = f"[green]{row['change_24h']:.2f}%[/green]" if row['change_24h'] >= 0 else f"[red]{row['change_24h']:.2f}%[/red]"
        c7d = f"[green]{row['change_7d']:.2f}%[/green]" if row['change_7d'] >= 0 else f"[red]{row['change_7d']:.2f}%[/red]"
        table.add_row(str(row['rank']), row['symbol'], f"R$ {row['price']:.2f}", c24, c7d, f"R$ {row['volume_24h']:.0f}", f"R$ {row['market_cap']:.0f}")

    console.print(table)
    status = "PRO" if is_pro() else "BETA"
    console.print(Panel.fit(f"Modo: {status} | Comandos: [bold]chart[/bold], [bold]portfolio[/bold], [bold]alerts[/bold], [bold]beta-watch[/bold], [bold]ai[/bold]", border_style="cyan"))

@app.command()
def chart(symbol: str, fiat: str = "BRL", days: int = 7, interval: str = "hourly"):
    """Desenha gráfico de linha no terminal (queda/subida ao longo do tempo)."""
    console.rule(f"[bold magenta]Gráfico {symbol.upper()} ({days}d, {interval})")
    times, prices = get_price_history(symbol.lower(), fiat.lower(), days=days, interval=interval)
    plot_line(times, prices, title=f"{symbol.upper()} - {fiat.upper()} ({days}d)", y_label=f"Preço ({fiat.upper()})")
    console.print(Panel("Linhas contínuas mostram tendência; quedas e altas ficam visíveis pela inclinação.", border_style="magenta"))

@app.command()
def beta_watch(symbol: str, fiat: str = "BRL", refresh: int = 20):
    """No BETA, dispara alerta a cada 3% de variação (queda ou subida)."""
    if is_pro():
        console.print("[yellow]Você está em PRO. Use alertas personalizados com o comando[/yellow] [bold]alert_add[/bold].")
    console.rule(f"[bold red]Beta Watch 3% - {symbol.upper()}")
    try:
        beta_watch_3pct(symbol=symbol.lower(), fiat=fiat.lower(), refresh_seconds=refresh, console=console)
    except KeyboardInterrupt:
        console.print("\n[cyan]Encerrado pelo usuário.[/cyan]")

@app.command()
def portfolio_add(symbol: str, qty: float, price: float, fiat: str = "BRL"):
    """Adiciona um ativo ao portfólio."""
    portfolio.add(symbol.upper(), qty, price, fiat)
    console.print(f"[green]Adicionado:[/green] {symbol.upper()} qty={qty} preço={fiat} {price}")

@app.command()
def portfolio_view():
    """Mostra o portfólio e P/L básico."""
    console.rule("[bold cyan]Portfólio")
    table = portfolio.table()
    console.print(table)

@app.command()
def alert_add(symbol: str, target: float, kind: str = "price"):
    """Cria um alerta (price | percent). Disponível completo no PRO."""
    if kind not in ("price", "percent"):
        typer.echo("kind precisa ser 'price' ou 'percent'")
        raise typer.Exit(code=1)
    alerts.add(symbol.upper(), target, kind)
    console.print(f"[yellow]Alerta criado[/yellow] {symbol.upper()} -> {kind} {target}")

@app.command()
def ai(question: str):
    """Pergunte à IA."""
    console.rule("[bold magenta]Assistente IA")
    answer = ask_ai(question)
    console.print(Panel(answer, border_style="magenta"))

@app.command()
def pro_status():
    """Verifica status Beta/Pro."""
    status = "PRO" if is_pro() else "BETA"
    console.print(Panel(f"Modo atual: {status}", border_style="green" if status == "PRO" else "red"))
    if not is_pro():
        console.print("Para desbloquear recursos PRO, acesse a página e conclua a assinatura.")

if __name__ == "__main__":
    app()
