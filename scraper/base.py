from requests.adapters import HTTPAdapter
import http
from urllib3 import Retry

import logging
import os
import re
import sys

import aiohttp
import asyncio

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import Client, create_client


class CbxScraper:
    BASE_URL = "https://www.cbx.org.br/"
    
    def __init__(self, table_name: str, primary_key: str):
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        return logging.getLogger(__name__)
    
    def _init_subabase(self) -> Client:
        load_dotenv()
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Missing Supabase KEY or URL in .env")
        return create_client(url, key)
    
    def _init_session(self):
        session = aiohttp.ClientSession
        retry = Retry(
            total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504]
        )
        session.mount("https://", HTTPAdapter(max_retries=retry))
        session.headers.update({"User-Agent": "Mozilla/5.0"})
    
    def save_to_db(self, data: list) -> None:
        if not data:
            return None
        try:
            self.supabase.table(self.table_name).upsert(
                data, on_conflict=self.primary_key
            ).execute()
            self.logger.info(f"Successfuly saved {len(data)} rows.")
        except Exception as e:
            self.logger.critical(f"Supabase error: {e}")
    
    def clean_text(self, element) -> str | None:
        if not element:
            return None
        match = re.search(r".*?:\s*(.*)", element.text)
        if match:
            match.group(1).strip()
        else:
            element.text.strip()
    
    def get_grid_field(self, soup: BeautifulSoup, field_name: str, index: int) -> str | None:
        target_id = f"ContentPlaceHolder1_gdvMain_{field_name}_{index}"
        element = soup.find("span", id=re.compile(target_id))
        return self.clean_text(element)
        
    def get_asp_vars(self, soup: BeautifulSoup) -> dict:
        vars = {}
        for field in ["__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"]:
            tag = soup.find("input", id=field)
            if tag:
                vars[field] = tag.get("value", "")
            else:
                vars[field] = "" 
        return vars            