import re
from datetime import datetime, timedelta, timezone

from base import Scraper
from bs4 import BeautifulSoup


class CBXAnnouncements(Scraper):
    def extract_page_data(self, soup: BeautifulSoup) -> list:
        page_notices = []
        rows = soup.find_all("tr")

        for row in rows:
            link_tag = row.find("a", id=re.compile(r"hlkTitulo"))
            date_tag = row.find("span", class_="date")

            if link_tag and date_tag:
                raw_date = date_tag.get_text(strip=True)

                clean_date = raw_date.replace("h", "")
                dt_obj = datetime.strptime(clean_date, "%d/%m/%Y %H:%M")
                tz_offset = timezone(timedelta(hours=-3))
                dt_tz = dt_obj.replace(tzinfo=tz_offset)
                iso_datetime = dt_tz.isoformat()

                href = link_tag.get("href", "")
                full_link = f"{self.DOMAIN.rstrip('/')}/{href.lstrip('/')}"
                announcement_id = (
                    href.split(f"{self.path}/")[1].split("/")[0]
                    if f"{self.path}/" in href
                    else None
                )

                page_notices.append(
                    {
                        "announcement_id": announcement_id,
                        "title": link_tag.get_text(strip=True),
                        "link": full_link,
                        "datetime": iso_datetime,
                    }
                )

        return page_notices

    def run(self):
        """Main execution logic for the scraper."""
        try:
            self.logger.info("Starting announcements extraction...")
            response = self.session.get(self.DOMAIN, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            self.logger.info(soup.prettify())
            current_page = 1

            while True:
                self.logger.info(f"Processing page {current_page}...")

                # Extraction and Persistence
                notices = self.extract_page_data(soup)
                self.save_to_db(notices)

                # ASP.NET Pagination Logic
                next_page = current_page + 1
                pagination_link = soup.find(
                    "a", href=re.compile(re.escape(f"Page${next_page}"))
                )
                all_links = soup.find_all("a", href=True)
                for link in all_links:
                    if "Page$" in link['href']:
                        self.logger.warning(f"Found potential link: {link['href']}")
                self.logger.warning(pagination_link)

                if pagination_link:
                    payload = self.get_asp_vars(soup)
                    payload.update(
                        {
                            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$gdvMain",
                            "__EVENTARGUMENT": f"Page${next_page}",
                        }
                    )

                    response = self.session.post(self.DOMAIN, data=payload, timeout=30)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, "html.parser")
                    current_page += 1
                else:
                    self.logger.info("Pagination reached the end.")
                    break

        except Exception as e:
            self.logger.critical(f"Unexpected error: {str(e)}", exc_info=True)


if __name__ == "__main__":
    scraper = CBXAnnouncements("announcements", "announcement_id", "comunicados")
    scraper.run()
