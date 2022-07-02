import asyncio

from parsers import HHParser


async def main():
    parser = HHParser(per_page=100)
    await parser.save_and_get_areas()
    await parser.load_all_vacancies()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
