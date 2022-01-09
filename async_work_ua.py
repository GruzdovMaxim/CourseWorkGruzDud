import asyncio
import time
import aiohttp

from bs4 import BeautifulSoup
from one_vacancy import OneVacancy
from useful_methods import get_busyness_num, get_ukr_city_name_by_rus
from translitua import translit

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}


async def gather_all_vacancies(arg_main_data, search_words, city_name, busyness):
    async with aiohttp.ClientSession() as session:
        link = f"https://work.ua/ru/jobs"
        if get_ukr_city_name_by_rus(city_name) is not None:
            link += f"-{translit(get_ukr_city_name_by_rus(city_name)).lower()}"
        link += f"-{search_words}/?"
        if get_busyness_num(busyness) is not None:
            link += f"employment={get_busyness_num(busyness) + 73}&"
        response = await session.get(link, headers=headers)

        the_soup = BeautifulSoup(await response.text(), "lxml")

        tasks = []
        if the_soup.find('ul', class_="pagination hidden-xs") is None:
            print(f"ВСЕГО ОДНА СТРАНИЦА")
            task = asyncio.create_task(get_page_vacancies(session, arg_main_data, link, 1))
            tasks.append(task)
        else:
            all_pages = int(the_soup.find('ul', class_="pagination hidden-xs").find_all("li")[-2].find('a').text)
            for page in range(1, all_pages + 1):
                temp = f"page={page}"
                task = asyncio.create_task(
                    get_page_vacancies(session, arg_main_data, link + temp, page))
                tasks.append(task)
        await asyncio.gather(*tasks)


async def get_page_vacancies(session, arg_main_data, arg_link, num_page):
    # await asyncio.sleep(0.4 + num_page * .1)
    arg_start_time = time.time()
    async with session.get(url=arg_link) as response:
        the_soup = BeautifulSoup(await response.text(), "lxml")

        blocks = the_soup.find_all("div", class_="card card-hover card-visited wordwrap job-link")

        page_vacancies = []
        for block in blocks:
            page_vacancies.append(
                OneVacancy(
                    block.find('h2').find().get("title").split(', вакансия')[0].strip(),
                    block.find('div', class_="add-top-xs").find('span').text.strip(),
                    block.find('div', class_="add-top-xs").find('span',
                                                                text="·").find_next().find_next().find_next().text
                    if block.find('div', class_="add-top-xs").find('span',
                                                                   text="·").find_next().text == "VIP" else block.find(
                        'div',
                        class_="add-top-xs").find('span', text="·").find_next().text,

                    block.find('p', class_="overflow text-muted add-top-sm cut-bottom").text.strip().replace(
                        "\n                           ", ""),
                    block.find('div', class_="row").find('span', class_="text-muted small").text,
                    "https://work.ua" + block.find('h2').find().get("href")
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
    all_vac = get_all_vacancies("Java", "Киев", "Любая занятость")
    for one_vacancy in all_vac:
        print(one_vacancy)
    print(len(all_vac), "вакансий")
    print("Время", time.time() - start_time)
