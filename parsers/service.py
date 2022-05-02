from .hh_parser import HHParser
from .regions_parser import RegionParser


def run_parser():
    hh = HHParser()
    first_page = hh.get_initial_data()
    pages = first_page.pages
    data = []
    for page in range(1, pages):
        data += hh.getPage(page)


def run_reg_parser():
    hh = HHParser()
    exit(hh.get_areas())


def run_region_parser():
    reg = RegionParser()
    exit(reg.get_city_codes())
