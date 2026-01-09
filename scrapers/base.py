import logging
import os
import re
import sys

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from supabase import Client, create_client
from urllib3.util.retry import Retry


class Scraper:
    def __init__(self, table: str, pk: str, path: str):
        self.logger = self._setup_logging()
        self.supabase = self._init_supabase()
        self.session = self._init_session()
        self.table: str = table
        self.pk: str = pk
        self.DOMAIN: str = "https://cbx.org.br/"
        self.path: str = f"https://cbx.org.br/{path}/"

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )
        return logging.getLogger(__name__)

    def _init_supabase(self) -> Client:
        load_dotenv()
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Missing Supabase credentials in .env")
        return create_client(url, key)

    def _init_session(self):
        session = requests.Session()
        retry = Retry(
            total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504]
        )
        session.mount("https://", HTTPAdapter(max_retries=retry))
        session.headers.update({"User-Agent": "Mozilla/5.0"})
        return session

    def get_asp_vars(self, soup: BeautifulSoup) -> dict:
        """Extracts hidden ASP.NET WebForms fields."""
        vars = {}
        for field in ["__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"]:
            tag = soup.find("input", id=field)
            vars[field] = tag.get("value", "") if tag else ""
        return vars

    def clean_text(self, element) -> str | None:
        """Extracts text after label (e.g., 'Label: Value' -> 'Value')."""
        if not element:
            return None
        match = re.search(r".*?:\s*(.*)", element.text)
        return match.group(1).strip() if match else element.text.strip()

    def get_grid_field(
        self, soup: BeautifulSoup, field_name: str, index: int
    ) -> str | None:
        """Finds a specific field in the ASP.NET GridView by index."""
        target_id = f"ContentPlaceHolder1_gdvMain_{field_name}_{index}"
        element = soup.find("span", id=re.compile(target_id))
        return self.clean_text(element)

    def save_to_db(self, data: list):
        """Upserts data into the configured Supabase table."""
        if not data:
            return
        try:
            self.supabase.table(self.table).upsert(data, on_conflict=self.pk).execute()
            self.logger.info(f"Successfully saved {len(data)} rows.")
        except Exception as e:
            self.logger.critical(f"Database error: {e}")
