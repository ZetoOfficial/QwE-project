from re import split as re_split

from lxml.html import fromstring
from parselab.cache import FileCache
from parselab.network import NetworkManager
from parselab.parsing import BasicParser
from settings import getLogger
from settings import settings as s

logger = getLogger(__name__)


class RegionParser(BasicParser):
    def __init__(self):
        self.cache = FileCache(namespace="russian-cities", path=s.app.cache_folder)
        self.net = NetworkManager()

    def get_city_codes(self) -> dict:
        """Получение кодов субъектов РФ

        Returns:
            dict: {субъект: код,}
        """
        page = self.get_page("https://ru.wikipedia.org/wiki/Коды_субъектов_Российской_Федерации")
        html = fromstring(page)
        city_codes = {}
        for tr in html.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr'):
            name = tr[0].text_content().strip()
            code = [re_split(r"\D+", code.strip())[0] for code in tr[1].text_content().strip().split(",")][0]
            city_codes[name.lower()] = code
        return city_codes
