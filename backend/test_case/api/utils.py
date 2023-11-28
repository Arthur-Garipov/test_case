import requests
from bs4 import BeautifulSoup


def parse_webpage(url):
    try:
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.660 YaBrowser/23.9.5.660 Yowser/2.5 Safari/537.36"
        }
        req = requests.get(url, headers=headers)
        src = req.text
        with open("index.html", "w", encoding="utf-8") as file:
            file.write(src)
        if req.status_code == 200:
            with open("index.html", encoding='utf-8') as file:
                sroc = file.read()
            soup = BeautifulSoup(sroc, "lxml")
            title = soup.find("title").text
            description = soup.find("meta", {'name': 'description'})
            if description:
                content = description.get('content')
            favicon = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
            if favicon:
                favicon = f'http://favicon.yandex.net/favicon/{url[8:]}'
                with open(f'{url[8:]}.jpg', 'wb') as file:
                    file.write(requests.get(url=favicon).content)
            return {
                'title': title,
                'description': content,
                'favicon': favicon,
                'url': url,
            }
        else:
            return {'error': 'Failed to retrieve the webpage', 'url': url}
    except Exception as e:
        return {'error': str(e), 'url': url}
