import asyncio
import time
import aiohttp

from bs4 import BeautifulSoup
from one_vacancy import OneVacancy
from useful_methods import get_busyness_num, get_ukr_city_name_by_rus

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}


async def gather_all_vacancies(arg_main_data, search_words, city_name, busyness):
    async with aiohttp.ClientSession() as session:
        link_part1 = f"https://rabota.ua/zapros/{search_words}/"
        if get_ukr_city_name_by_rus(city_name) is None:
            city_name = "украина"
        link_part1 += f"{city_name.lower()}"
        link_part2 = ""
        if get_busyness_num(busyness) is not None:
            link_part2 += f"?scheduleId={get_busyness_num(busyness)}"
        response = await session.get(url=link_part1 + link_part2, headers=headers)
        the_soup = BeautifulSoup(await response.text(), "lxml")

        if the_soup.find('span', class_="fd-fat-merchant").text == 0:
            return

        tasks = []
        if len(the_soup.find_all("dd")) == 0:
            print(f"ВСЕГО ОДНА СТРАНИЦА")
            task = asyncio.create_task(get_page_vacancies(session, arg_main_data, link_part1 + link_part2, 1))
            tasks.append(task)
        else:
            all_pages = int(the_soup.find_all("dd")[-2].find('a').text)
            for page in range(1, all_pages + 1):
                temp = ""
                if page > 1:
                    temp = f"/pg{page}"
                task = asyncio.create_task(
                    get_page_vacancies(session, arg_main_data, link_part1 + temp + link_part2, page))
                tasks.append(task)
        await asyncio.gather(*tasks)


async def get_page_vacancies(session, arg_main_data, arg_link, num_page):
    # await asyncio.sleep(0.4 + num_page * .1)
    arg_start_time = time.time()
    async with session.get(url=arg_link, headers=headers) as response:
        the_soup = BeautifulSoup(await response.text(), "lxml")

        blocks = the_soup.find_all("tr")
        if blocks[-1].find('div', class_="bottom-recommended-block") is None:
            blocks.pop(len(blocks) - 1)

        page_vacancies = []
        for block in blocks:
            page_vacancies.append(
                OneVacancy(
                    block.find('h2', class_="card-title").text.strip(),
                    block.find('p', class_="company-name").text.strip(),
                    block.find('span', class_="location").text.strip(),
                    block.find('div', class_="card-description").text.strip(),
                    block.find('div', class_="card-footer").find().text.strip(),
                    "https://rabota.ua" + block.find('h2', class_="card-title").find().get("href")
                )
            )
        print(f"Обработано({arg_link})")
        print("Время", time.time() - arg_start_time)

        arg_main_data += page_vacancies


def get_all_vacancies(search_words, city_name, busyness):
    main_data = []
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gather_all_vacancies(main_data, search_words, city_name, busyness))
    return main_data


if __name__ == '__main__':
    start_time = time.time()
    data_vacancies = get_all_vacancies("java", "Львов", "Удаленная работа")
    for one_vacancy in data_vacancies:
        print(one_vacancy)
    print(len(data_vacancies), "вакансий")
    print("Время", time.time() - start_time)
