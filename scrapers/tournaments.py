import re

from bs4 import BeautifulSoup

from .base import Scraper


class CBXTournaments(Scraper):
    def extract_page_data(self, soup: BeautifulSoup) -> list:
        """Extracts data from each tournament table on the current page."""
        tables = soup.find_all("table", attrs={"class": "torneios"})
        page_tournaments = []

        for i in range(len(tables)):
            reg_elem = soup.find(
                "a", id=re.compile(f"ContentPlaceHolder1_gdvMain_hlkTorneio_{i}")
            )

            regulation_path = reg_elem.get("href") if reg_elem else None

            page_tournaments.append(
                {
                    "title": self.get_grid_field(soup, "lblNomeTorneio", i),
                    "cbx_id": self.get_grid_field(soup, "lblIDTorneio", i),
                    "organizer": self.get_grid_field(soup, "lblOrganizador", i),
                    "location": self.get_grid_field(soup, "lblLocal", i),
                    "period": self.get_grid_field(soup, "lblPeriodo", i),
                    "notes": self.get_grid_field(soup, "lblObs", i),
                    "regulation_url": (self.DOMAIN + str(regulation_path))
                    if regulation_path
                    else None,
                    "status": self.get_grid_field(soup, "lblStatus", i),
                    "rhythm": self.get_grid_field(soup, "lblRitmo", i),
                    "rating": self.get_grid_field(soup, "lblRating", i),
                    "players_count": self.get_grid_field(soup, "lblQtJogadores", i),
                    "fide_players_count": self.get_grid_field(
                        soup, "lblQtJogadoresFIDE", i
                    ),
                }
            )

        return page_tournaments

    def run(self, year: str, month: str):
        """Main execution loop for the scraper."""
        try:
            self.logger.info(f"Starting tournament extraction for {month}/{year}...")
            response = self.session.get(self.path, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Initial filters setup
            payload = self.get_asp_vars(soup)
            payload.update(
                {
                    "__EVENTTARGET": "ctl00$ContentPlaceHolder1$cboMes",
                    "ctl00$ContentPlaceHolder1$cboAno": year,
                    "ctl00$ContentPlaceHolder1$cboMes": month,
                }
            )

            current_page = 1
            while True:
                self.logger.info(f"Processing page {current_page}...")
                response = self.session.post(self.path, data=payload, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                # Extract and Save
                tournaments = self.extract_page_data(soup)
                self.save_to_db(tournaments)

                # Pagination logic
                next_page = current_page + 1
                next_page_link = soup.find("a", href=re.compile(rf"Page\${next_page}"))

                if next_page_link:
                    payload = self.get_asp_vars(soup)
                    payload.update(
                        {
                            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$gdvMain",
                            "__EVENTARGUMENT": f"Page${next_page}",
                            "ctl00$ContentPlaceHolder1$cboAno": year,
                            "ctl00$ContentPlaceHolder1$cboMes": month,
                        }
                    )
                    current_page += 1
                else:
                    self.logger.info("Pagination reached the end.")
                    break

        except Exception as e:
            self.logger.critical(f"Unexpected error: {str(e)}", exc_info=True)


if __name__ == "__main__":
    scraper = CBXTournaments("tournaments", "cbx_id", "torneios")
    scraper.run()
