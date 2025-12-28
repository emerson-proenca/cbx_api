import re

from base import WebFormsScraper
from bs4 import BeautifulSoup


class CBXScraper(WebFormsScraper):
    def __init__(self, target_state: str = "SE"):
        # Initialize parent with Supabase table details
        super().__init__(table_name="players", primary_key="cbx_id")
        self.base_url = "https://www.cbx.org.br/rating"
        self.target_state = target_state

    def extract_page_data(self, soup: BeautifulSoup) -> list:
        """Parses the rating table for player data."""
        table = soup.find("table", id="ContentPlaceHolder1_gdvMain")
        if not table:
            return []

        players = []
        for row in table.find_all("tr"):
            cols = row.find_all("td")

            # Validate player row (minimum 8 columns and contains an ID link)
            if len(cols) >= 8:
                id_link = cols[0].find("a")
                if id_link and "/jogador/" in id_link.get("href", ""):
                    players.append(
                        {
                            "cbx_id": id_link.text.strip(),
                            "name": cols[1].text.strip(),
                            "birth_date": cols[2].text.strip(),
                            "state": cols[3].text.strip(),
                            "fide_id": cols[4].text.strip(),
                            "classical": cols[5].text.strip(),
                            "rapid": cols[6].text.strip(),
                            "blitz": cols[7].text.strip(),
                        }
                    )
        return players

    def run(self):
        """Main execution flow for scraping and pagination."""
        try:
            # 1. Initial GET and State selection
            response = self.session.get(self.base_url)
            soup = BeautifulSoup(response.text, "html.parser")

            payload = self.get_asp_vars(soup)
            payload.update(
                {
                    "__EVENTTARGET": "ctl00$ContentPlaceHolder1$cboUF",
                    "ctl00$ContentPlaceHolder1$cboUF": self.target_state,
                }
            )

            current_page = 1
            while True:
                self.logger.info(
                    f"Processing page {current_page} for {self.target_state}..."
                )

                # Fetch page content
                response = self.session.post(self.base_url, data=payload)
                soup = BeautifulSoup(response.text, "html.parser")

                # 2. Extract and Save
                players = self.extract_page_data(soup)
                self.save_to_db(players)

                # 3. Pagination Logic
                next_page_num = current_page + 1
                next_page_link = soup.find(
                    "a", href=re.compile(rf"Page\${next_page_num}")
                )

                if next_page_link:
                    payload = self.get_asp_vars(soup)
                    payload.update(
                        {
                            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$gdvMain",
                            "__EVENTARGUMENT": f"Page${next_page_num}",
                            "ctl00$ContentPlaceHolder1$cboUF": self.target_state,
                        }
                    )
                    current_page += 1
                else:
                    self.logger.info("Reached the end of the list.")
                    break

        except Exception as e:
            self.logger.error(f"Execution error: {e}")


if __name__ == "__main__":
    scraper = CBXScraper(target_state="SE")
    scraper.run()
