import requests


class API:
    def __init__(self, api_url, organization_slug, department_slug, token):
        self.API_URL = api_url
        self._organization_and_department_slug = f'{organization_slug}/{department_slug}/'
        self.categories_url = self.API_URL + 'categories/' + self._organization_and_department_slug
        self.category_url = self.API_URL + 'category/' + self._organization_and_department_slug
        self.questions_url = self.API_URL + 'questions/' + self._organization_and_department_slug
        self.question_url = self.API_URL + 'question/' + self._organization_and_department_slug
        self._headers = {
            'Bot-Authorization': token
        }

    def get_categories(self, category_id: int = None) -> list:
        if category_id == '0':
            category_id = None
        url = self.categories_url + f'{category_id}/' if category_id else self.categories_url
        response = requests.get(url, headers=self._headers)

        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()

        categories = response.json()
        return categories

    def get_category_info(self, category_id: int) -> dict:
        """Получение информации о категории по id"""
        url = self.category_url + f'{category_id}/'
        response = requests.get(url, headers=self._headers)

        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()

        category = response.json()
        return category

    def get_questions(self, category_id: int) -> list:
        """Получение списка вопросов по id"""
        url = self.questions_url + f'{category_id}/'
        response = requests.get(url, headers=self._headers)

        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()

        questions = response.json()
        return questions

    def get_question_info(self, question_id) -> dict:
        """Получение информации о вопросе по id"""
        url = self.question_url + f'{question_id}/'
        response = requests.get(url, headers=self._headers)

        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()

        question = response.json()
        return question
