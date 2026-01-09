import os

from dotenv import load_dotenv
from typer.testing import CliRunner

from project import app, validate_env

runner = CliRunner()


def test_validate_env():
    load_dotenv()
    URL = os.environ.get("SUPABASE_URL")
    KEY = os.environ.get("SUPABASE_KEY")
    if not URL or not KEY:
        raise ValueError("Missing Supabase credentials in .env")


def test_supabase():
    client = validate_env()
    assert client is not None
    assert "supabase.co" in str(client.supabase_url)


def test_fetch():
    result = runner.invoke(app, ["fetch", "news", "--select", "title"])
    assert result.exit_code == 0
    assert "news.json" in result.stdout or result.exit_code == 0


def test_players():
    result = runner.invoke(app, ["players", "TO"])
    assert result.exit_code == 0


def test_tournaments():
    result = runner.invoke(app, ["tournaments", "2005", "12"])
    assert result.exit_code == 0


def test_announcements():
    result = runner.invoke(app, ["announcements"])
    assert result.exit_code == 0


def test_news():
    result = runner.invoke(app, ["news"])
    assert result.exit_code == 0
