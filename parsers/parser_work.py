import requests
from bs4 import BeautifulSoup
import sqlite3


def work_parser():
    print('work parser')
    db = sqlite3.connect('vacancies.db')
    sql = db.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS work (
        Url TEXT,
        City TEXT,
        Company TEXT,
        Position TEXT
    )""")
    db.commit()

    sql.execute('DELETE FROM work')

    HOST = 'https://www.work.ua'
    jobs_name_list = ['trainee+python',
                      'junior+python',
                      'python+back+end+developer',
                      'python+trainee+developer']

    card_url_list = []

    for jobs_name in jobs_name_list:
        page = '/'
        i = 1
        card_url_list.append(['--------', f'{jobs_name}', '--------', '--------'])
        print(jobs_name)
        while True:
            url = f'https://www.work.ua/jobs-{jobs_name}{page}'
            i += 1
            page = f'/?page={i}'
            r = requests.get(url)
            result = r.content
            soup = BeautifulSoup(result, 'html.parser')
            cards = soup.find_all(class_='card-hover')

            if not cards:
                break

            for card in cards:
                job_list = []
                card_url = HOST + card.find('a').get('href')
                card_title = card.find('a').text
                card_title = card_title.strip(u'\u200b')
                company_info = card.find(class_='add-top-xs').text
                company_name_and_location = (company_info.replace('\xa0', ' ').replace('\xdc', 'U').strip().split('·'))

                company_name = company_name_and_location[0]
                if company_name_and_location[1] == ' VIP ':
                    company_location = company_name_and_location[2]
                else:
                    company_location = company_name_and_location[1]

                job_list.append(card_url)
                job_list.append(company_location)
                job_list.append(company_name)
                job_list.append(card_title)

                if job_list not in card_url_list:
                    card_url_list.append(job_list)


    for line in card_url_list:
        sql.execute('INSERT INTO work VALUES (?, ?, ?, ?)', (line[0], line[1], line[2], line[3]))
        db.commit()




