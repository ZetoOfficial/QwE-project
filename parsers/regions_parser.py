from lxml.html import fromstring

from parselab.parsing import BasicParser
from parselab.network import NetworkManager
from parselab.cache import FileCache

from app.crud import create_area
from app.schemas import Area
from settings import settings as s, getLogger
from time import sleep
import re


logger = getLogger(__name__)


class RegionParser(BasicParser):

    data = list()

    def __init__(self):
        self.cache = FileCache(namespace="russian-cities", path=s.app.cache_folder)
        self.net = NetworkManager()

    def sleep(self):
        logger.info("Sleeping for %s s" % 0)
        sleep(0)

    def get_code(self, url) -> str:
        page = self.get_page(url)
        html = fromstring(page)
        try:
            code = (
                html.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[31]/td')[0]
                .text_content()
                .strip()
            )
        except IndexError:
            return "-1"
        return code

    def run(self):
        page = self.get_page("https://ru.wikipedia.org/wiki/Список_городов_России")
        html = fromstring(page)

        for tr in html.xpath("//table/tbody/tr"):
            columns = tr.xpath(".//td")
            if len(columns) != 9:
                continue
            url = columns[2].xpath("./a")[0].get("href")
            area = {
                "code": self.get_code(f"https://ru.wikipedia.org{url}"),
                "region": columns[3].text_content().strip(),
                "city": columns[2].xpath("./a")[0].text_content().strip(),
            }
            area_dto = create_area(Area.parse_obj(area))
            logger.info(f"{area_dto.code} {area_dto.region} {area_dto.city}")

    def get_city_codes(self) -> dict:
        page = self.get_page("https://ru.wikipedia.org/wiki/Коды_субъектов_Российской_Федерации")
        html = fromstring(page)
        city_codes = {}
        for tr in html.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr'):
            name = tr[0].text_content().strip()
            code = [re.split(r"\D+", code.strip())[0] for code in tr[1].text_content().strip().split(",")][0]
            print(name, code)
            city_codes[name] = code
        return city_codes


if __name__ == "__main__":
    app = RegionParser()
    exit(app.run())
