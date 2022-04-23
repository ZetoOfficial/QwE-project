from parser.hh_parser import HHParser


def run_parser():
    hh = HHParser()
    first_page = hh.get_initial_data()
    pages = first_page.pages
    data = []
    for page in range(1, pages):
        data += hh.getPage(page)
