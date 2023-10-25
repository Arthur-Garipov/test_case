import requests
from bs4 import BeautifulSoup


def parse_webpage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else ""
            description = soup.find('meta', attrs={'name': 'description'})
            description = description['content'] if description else ""
            favicon = soup.find('link', attrs={'rel': 'icon'})
            favicon = favicon['href'] if favicon else ""
            return {
                'title': title,
                'description': description,
                'favicon': favicon,
                'url': url,
            }
        else:
            return {'error': 'Failed to retrieve the webpage', 'url': url}
    except Exception as e:
        return {'error': str(e), 'url': url}
