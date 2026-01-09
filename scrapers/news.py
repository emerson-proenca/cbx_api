import re
from datetime import datetime, timedelta, timezone

from bs4 import BeautifulSoup

from .base import Scraper


class CBXNews(Scraper):
    def extract_page_data(self, soup: BeautifulSoup) -> list[dict]:
        """Parses the news table for titles, links, and dates."""
        news_list = []
        for row in soup.find_all("tr"):
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
                news_id = (
                    href.split("noticia/")[1].split("/")[0]
                    if "noticia/" in href
                    else None
                )
                news_list.append(
                    {
                        "news_id": news_id,
                        "title": link_tag.text.strip(),
                        "link": full_link,
                        "datetime": iso_datetime,
                    }
                )
        return news_list

    def run(self):
        """Main execution loop for pagination and data storage."""
        response = self.session.get(self.path)
        soup = BeautifulSoup(response.text, "html.parser")
        current_page = 1

        while True:
            self.logger.info(f"Processing page {current_page}...")
            news_data = self.extract_page_data(soup)

            # Use the inherited save_to_db method
            self.save_to_db(news_data)

            # Check for next page link
            next_page = current_page + 1
            next_page_btn = soup.find("a", href=re.compile(rf"Page\${next_page}"))

            if next_page_btn:
                # Use inherited get_asp_vars for WebForms state
                payload = self.get_asp_vars(soup)
                payload.update(
                    {
                        "__EVENTTARGET": "ctl00$ContentPlaceHolder1$gdvMain",
                        "__EVENTARGUMENT": f"Page${next_page}",
                    }
                )

                response = self.session.post(self.path, data=payload)
                soup = BeautifulSoup(response.text, "html.parser")
                current_page += 1
            else:
                self.logger.info("No more pages found.")
                break


if __name__ == "__main__":
    scraper = CBXNews("news", "news_id", "noticias")
    scraper.run()
