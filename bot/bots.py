import requests
from .secrets import Secret
import random


class BigBot:
    """
    In this bot I've realized all of the basic capabilities of the telegram bots
    """

    def __init__(self, token, data, name=None):
        # token for API access
        self.token = token

        # url to access the API
        self.url = 'https://api.telegram.org/bot%s/' % self.token

        # JSON data with Update object
        self.data = data

        # name of the bot
        self.name = name

    # chat info
    @property
    def current_chat_id(self):
        try:
            chat_id = self.data['message']['chat']['id']
            return chat_id
        except KeyError:
            return None

    @property
    def name_of_interlocutor(self):
        try:
            name = self.data['message']['chat']['first_name']
            return name
        except KeyError:
            return None

    @property
    def username_of_interlocutor(self):
        try:
            name = self.data['message']['chat']['username']
            return name
        except KeyError:
            return None

    @property
    def text(self):
        try:
            name = self.data['message']['text']
            return name
        except KeyError:
            return None

    # sending
    def _send(self, type_to_send, what_to_send, url_to_send, chat_id=None):
        chat_id = chat_id or self.current_chat_id
        response = requests.get(self.url + url_to_send,
                                {'chat_id': chat_id, type_to_send: what_to_send})
        if response.status_code == 200:
            return True
        else:
            return False

    def send_text(self, text, chat_id=None):
        response = self._send('text', text, 'sendMessage', chat_id=chat_id)

        return response

    def send_photo(self, photo_url, chat_id=None):
        response = self._send('photo', photo_url, 'sendPhoto', chat_id=chat_id)

        return response

    def __str__(self):
        return '<Bot object with name: %s>' % self.name or 'unknown'

    def __len__(self):
        return 1


class SecretBot(BigBot):
    """
    This bot will be used to hide the Secret and Big Bot's interaction mechanism
    """
    def __init__(self, token, data, name=None):
        super().__init__(token, data, name)

        self.secret = Secret(self.get_number)

        print('AAAAAAAAAAAAAAAAAAAAA: ', self.secret.photo)

    # generate information
    @property
    def get_number(self):
        return random.randint(1, 23410)

    # compose messages

    def compose_message(self):
        title = self.secret.title
        description = self.secret.description
        models = self.secret.model
        categories = self.secret.categories
        url = self.secret.link

        template = """
        Итак, магия!
%s
        
%s
        
Модели: 
%s
        
Категории: 
%s
        
И самое важное)
Ссылка: %s""" % (title, description,
                         models, categories, url)

        return template

    def send_secret(self, chat_id=None):
        chat_id = chat_id or self.current_chat_id
        response = requests.get(self.url + 'sendPhoto',
                                {'chat_id': chat_id, 'photo': self.secret.photo,
                                 'caption': self.compose_message()})
        if response.status_code == 200:
            return True
        else:
            return False
