import os


class Environment:

    DEV = 'dev'
    PROD = 'prod'
    URLS = {
        PROD: 'https://playground.learnqa.ru/api',
        DEV: 'https://playground.learnqa.ru/api_dev'

    }

    def __init__(self):
        try:
            self.env = os.environ['ENV']
        except KeyError:
            self.env = self.PROD

    def get_base_url(self):
        if self.env in self.URLS:
            return self.URLS[self.env]
        else:
            raise Exception(f"Unkown value of ENV variable{self.env}")


ENV_OBJECT = Environment()
