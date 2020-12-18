import requests
from bs4 import BeautifulSoup
import sqlite3


def rabota_parser():
    print('rabota parser')
    db = sqlite3.connect('vacancies.db')
    sql = db.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS rabota (
        Url TEXT,
        City TEXT,
        Company TEXT,
        Position TEXT
    )""")
    db.commit()

    sql.execute('DELETE FROM rabota')

    HOST = 'https://rabota.ua'
    jobs_name_list = ['trainee-python',
                      'junior-python',
                      'python-back-end-developer',
                      'python-trainee-developer']

    card_url_list = []

    for jobs_name in jobs_name_list:
        page = '/'
        i = 1
        card_url_list.append(['--------', f'{jobs_name}', '--------', '--------'])
        print(jobs_name)
        while True:
            url = f'https://rabota.ua/zapros/{jobs_name}/%d1%83%d0%ba%d1%80%d0%b0%d0%b8%d0%bd%d0%b0{page}'
            i += 1
            page = f'/pg{i}'
            r = requests.get(url)
            result = r.content
            soup = BeautifulSoup(result, 'html.parser')
            cards = soup.find_all(class_='common-info')

            if not cards:  # if cards == []:
                break

            for card in cards:
                job_list = []
                card_url = HOST + card.find(class_='ga_listing').get('href')
                card_title = card.find(class_='ga_listing').get('title')
                company_name = card.find(class_='company-profile-name').get('title')
                location = card.find(class_='location').text

                job_list.append(card_url)
                job_list.append(location)
                job_list.append(company_name)
                job_list.append(card_title)

                if job_list not in card_url_list:
                    card_url_list.append(job_list)

    for line in card_url_list:
        sql.execute('INSERT INTO rabota VALUES (?, ?, ?, ?)', (line[0], line[1], line[2], line[3]))
        db.commit()

