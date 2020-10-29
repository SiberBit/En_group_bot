import requests


class API:
    def __init__(self, api_url):
        self.API_URL = api_url
        self.categories_url = self.API_URL + 'categories/'
        self.category_url = self.API_URL + 'category/'

    def get_categories(self, category_id: int = None) -> list:
        if category_id == '0':
            category_id = None

        response = requests.get(self.categories_url + f'{category_id}/' if category_id else self.categories_url)

        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()

        categories = response.json()
        return categories

    def get_category_info(self, category_id: int):
        """Получение информации о категории по id"""
        response = requests.get(self.category_url + f'{category_id}/')

        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()

        category = response.json()
        return category
