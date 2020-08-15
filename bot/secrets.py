import bs4
import requests


class Secret:
    """
    This is a class to manage content,
    which we are going to get from a secret site
    """

    def __init__(self, number):
        # we'll be looking for a video with this number
        self.number = number

        # url to access the secret site
        self.url = 'http://porno365.fun/movie/' + str(self.number)

        # content
        self.soup = bs4.BeautifulSoup(self._get_content(), 'html.parser')

    # content scraping
    def _get_content(self):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/83.0.4103.97 Safari/537.36"}

        response = requests.get(self.url, headers=headers)
        content = response.content.decode('utf-8')

        return content

    # content processing
    @property
    def photo(self):
        links = self.soup.find_all('link')

        url = None

        for link in links:
            try:
                if link['itemprop'] == 'contentUrl':
                    url = link['href']
            except KeyError:
                continue

        return url

    @property
    def description(self):
        divs = self.soup.find_all('div')

        desc = None

        for div in divs:
            try:
                if div['itemprop'] == 'description':
                    desc = div.string
            except KeyError:
                continue

        return desc

    @property
    def model(self):
        links = self.soup.find_all('a')

        model = None

        for link in links:
            try:
                if link['class'] == ['model_link']:
                    model = link.string
            except KeyError:
                continue

        return model

    @property
    def categories(self):
        divs = self.soup.find_all('div')

        categories = []

        for div in divs:
            try:
                if div['class'] == ['video-categories'] and div.string != 'Модели:':
                    for a in div.find_all('a'):
                        categories.append(a.string)
                    break
            except KeyError:
                continue

        return ', '.join(categories)

    @property
    def title(self):
        hs = self.soup.find_all('h1')

        title = None

        for h in hs:
            try:
                if h['itemprop'] == 'name':
                    title = h.string
            except KeyError:
                continue

        return title

    @property
    def link(self):
        return self.url
