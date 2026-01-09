import typer

from scrapers.announcements import CBXAnnouncements
from scrapers.news import CBXNews
from scrapers.players import CBXPlayers
from scrapers.tournaments import CBXTournaments

app = typer.Typer()


@app.command()
def players(
    target_state: str,
    table_name="players",
    primary_key: str = "cbx_id",
    path: str = "rating",
):
    scraper = CBXPlayers(table_name, primary_key, path)
    scraper.run(target_state=target_state)


@app.command()
def news(
    table_name: str = "news", primary_key: str = "news_id", path: str = "noticias"
):
    scraper = CBXNews(table_name, primary_key, path)
    scraper.run()


@app.command()
def announcements(
    table_name: str = "announcements",
    primary_key: str = "announcement_id",
    path: str = "comunicados",
):
    scraper = CBXAnnouncements(table_name, primary_key, path)
    scraper.run()


@app.command()
def tournaments(
    year: str,
    month: str,
    table_name: str = "tournaments",
    primary_key: str = "cbx_id",
    path: str = "torneios",
):
    scraper = CBXTournaments(table_name, primary_key, path)
    scraper.run(year, month)


if __name__ == "__main__":
    app()
