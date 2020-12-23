import requests
from bs4 import BeautifulSoup


class WorkParser:
    card_vacancies_list = []

    def __init__(self, jobs_name, page):
        self.URL = 'https://www.work.ua'
        self.jobs_name = jobs_name
        self.page = page

    def get_html(self):
        url = f'{self.URL}/jobs-{self.jobs_name}{self.page}'
        r = requests.get(url)
        return r

    def get_soup_cards(self):
        result = self.get_html().content
        soup = BeautifulSoup(result, 'html.parser')
        cards = soup.find_all(class_='card-hover')
        if not cards:
            return 0

        return cards

    def get_content(self):
        for card in self.get_soup_cards():
            job_list = []
            card_url = self.URL + card.find('a').get('href')
            card_title = card.find('a').text
            card_title = card_title.strip(u'\u200b')
            company_info = card.find(class_='add-top-xs').text
            company_name_and_location = (company_info.strip().split('·'))

            company_name = company_name_and_location[0]
            if company_name_and_location[1] == ' VIP ':
                company_location = company_name_and_location[2]
            else:
                company_location = company_name_and_location[1]

            job_list.append(card_url)
            job_list.append(company_location)
            job_list.append(company_name)
            job_list.append(card_title)

            if job_list not in self.card_vacancies_list:
                self.card_vacancies_list.append(job_list)
        return self.card_vacancies_list


class WorkContent:
    jobs_list = []
    jobs_name_list = ['trainee+python',
                      'junior+python',
                      'python+back+end+developer',
                      'python+trainee+developer']

    def get_info(self):
        for jobs_name in self.jobs_name_list:
            print(f'work.ua: {jobs_name}')
            self.jobs_list.append([jobs_name, '', '', ''])
            content_iterator = 1
            page = ''
            while True:
                if not WorkParser(jobs_name, page).get_soup_cards():
                    break
                content = WorkParser(jobs_name, page).get_content()

                content_iterator += 1
                page = f'/?page={content_iterator}'

                for item in content:
                    if item not in self.jobs_list:
                        self.jobs_list.append(item)
        return self.jobs_list
