import json
import os

import typer
from dotenv import load_dotenv
from supabase import Client, create_client

from scrapers.announcements import CBXAnnouncements
from scrapers.news import CBXNews
from scrapers.players import CBXPlayers
from scrapers.tournaments import CBXTournaments

app = typer.Typer()


@app.callback()
def main():
    validate_env()


@app.command()
def fetch(table: str, select: str = "*"):
    """SELECTS what data from TABLE in Supabase to FETCH.

    Args:
        table (str): Name of the TABLE to fetch data from
        select (str, optional): SELECT what data to fetch. Defaults to "*".
    """
    supabase: Client = validate_env()
    response = supabase.table(table).select(select).execute()

    with open(f"{table}.json", "w", encoding="utf-8") as f:
        json.dump(response.data, f, indent=4, ensure_ascii=False)


# WEBSCRAPING COMMANDS
@app.command()
def players(
    state: str,
    table: str = "players",
    pk: str = "cbx_id",
    path: str = "rating",
):
    """Scrapes PLAYERS in STATE from https://cbx.org.br/rating

    Args:
        tate (str): Name of the STATE to scrape data from.
        table (str, optional): Name of the TABLE to save data to Supabase. Defaults to "players".
        pk (str, optional): Name of the PRIMARY KEY to upsert data to TABLE. Defaults to "cbx_id".
        path (str, optional): PATH of the URL. Defaults to "rating".
    """
    scraper = CBXPlayers(table, pk, path)
    scraper.run(target_state=state)


@app.command()
def news(table: str = "news", pk: str = "news_id", path: str = "noticias"):
    """Scrapes NEWS from https://cbx.org.br/noticias

    Args:
        table (str, optional): Name of the TABLE to save data to Supabase. Defaults to "news".
        pk (str, optional): Name of the PRIMARY KEY to upsert data to TABLE. Defaults to "news_id".
        path (str, optional): PATH of the URL. Defaults to "noticias".
    """
    scraper = CBXNews(table, pk, path)
    scraper.run()


@app.command()
def announcements(
    table: str = "announcements",
    pk: str = "announcement_id",
    path: str = "comunicados",
):
    """Scrapes ANNOUNCEMENTS from https://cbx.org.br/comunicados

    Args:
        table (str, optional): Name of the TABLE to save data to Supabase. Defaults to "announcements".
        pk (str, optional): Name of the PRIMARY KEY to upsert data to TABLE. Defaults to "announcement_id".
        path (str, optional): PATH of the URL. Defaults to "comunicados".
    """
    scraper = CBXAnnouncements(table, pk, path)
    scraper.run()


@app.command()
def tournaments(
    year: str,
    month: str,
    table: str = "tournaments",
    pk: str = "cbx_id",
    path: str = "torneios",
):
    """Scrapes TOURNAMENTS in MONTH/YEAR from https://cbx.org.br/torneios

    Args:
        year (str): Name of the YEAR to scrape data from.
        month (str): Name of the MONTH to scrape data from.
        table (str, optional): Name of the TABLE to save data to Supabase. Defaults to "tournaments".
        pk (str, optional): Name of the PRIMARY KEY to upsert data to TABLE. Defaults to "cbx_id".
        path (str, optional): PATH of the URL. Defaults to "torneios".
    """
    scraper = CBXTournaments(table, pk, path)
    scraper.run(year, month)


def validate_env() -> Client:
    load_dotenv()
    URL = os.environ.get("SUPABASE_URL")
    KEY = os.environ.get("SUPABASE_KEY")
    if not URL or not KEY:
        raise ValueError("Missing Supabase credentials in .env")
    return create_client(URL, KEY)


if __name__ == "__main__":
    app()
