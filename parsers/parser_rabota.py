import requests
from bs4 import BeautifulSoup


class RabotaParser:
    card_vacancies_list = []

    def __init__(self, jobs_name, page):
        self.URL = 'https://rabota.ua'
        self.jobs_name = jobs_name
        self.page = page

    def get_html(self):
        url = f'{self.URL}/zapros/{self.jobs_name}/украина{self.page}'
        r = requests.get(url)
        return r

    def get_soup_cards(self):
        result = self.get_html().content
        soup = BeautifulSoup(result, 'html.parser')
        cards = soup.find_all(class_='common-info')
        if not cards:
            return 0

        return cards

    def get_content(self):
        for card in self.get_soup_cards():
            job_list = []
            card_url = self.URL + card.find(class_='ga_listing').get('href')
            card_title = card.find(class_='ga_listing').get('title')
            company_name = card.find(class_='company-profile-name').get('title')
            location = card.find(class_='location').text

            job_list.append(card_url)
            job_list.append(location)
            job_list.append(company_name)
            job_list.append(card_title)

            if job_list not in self.card_vacancies_list:
                self.card_vacancies_list.append(job_list)
        return self.card_vacancies_list


class RabotaContent:
    jobs_list = []
    jobs_name_list = ['trainee-python',
                      'junior-python',
                      'python-back-end-developer',
                      'python-trainee-developer']

    def get_info(self):
        for jobs_name in self.jobs_name_list:
            print(f'rabota.ua: {jobs_name}')
            self.jobs_list.append([jobs_name, '', '', ''])
            content_iterator = 1
            page = ''
            while True:
                if not RabotaParser(jobs_name, page).get_soup_cards():
                    break
                content = RabotaParser(jobs_name, page).get_content()

                content_iterator += 1
                page = f'/pg{content_iterator}'

                for item in content:
                    if item not in self.jobs_list:
                        self.jobs_list.append(item)
        return self.jobs_list
