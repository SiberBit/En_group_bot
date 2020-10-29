import requests


class API:
    def __init__(self, api_url):
        self.API_URL = api_url
        self.categories_url = self.API_URL + 'categories/'
        self.category_url = self.API_URL + 'category/'
        self.questions_url = self.API_URL + 'questions/'
        self.question_url = self.API_URL + 'question/'


    def get_categories(self, category_id: int = None) -> list:
        if category_id == '0':
            category_id = None

        response = requests.get(self.categories_url + f'{category_id}/' if category_id else self.categories_url)

        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()

        categories = response.json()
        return categories

    def get_category_info(self, category_id: int) -> dict:
        """Получение информации о категории по id"""
        response = requests.get(self.category_url + f'{category_id}/')

        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()

        category = response.json()
        return category

    def get_questions(self, category_id: int) -> list:
        """Получение списка вопросов по id"""
        response = requests.get(self.questions_url + f'{category_id}/')

        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()

        questions = response.json()
        return questions

    def get_question_info(self, question_id) -> dict:
        """Получение информации о вопросе по id"""
        response = requests.get(self.question_url + f'{question_id}/')

        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()

        question = response.json()
        return question
