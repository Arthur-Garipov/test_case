from django.core.exceptions import PermissionDenied, ValidationError
from django.core.validators import URLValidator
from django.shortcuts import get_object_or_404, redirect, render
import requests
from bs4 import BeautifulSoup
from .models import Bookmark


def delete_bookmark(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark, id=bookmark_id)
    bookmark.delete()
    return redirect('list_bookmarks')


def list_bookmarks(request):
    bookmarks = Bookmark.objects.all()
    error_message = None

    if request.method == 'POST':
        url = request.POST.get('url')

        # Валидация URL и проверка на наличие в базе
        url_validator = URLValidator()
        try:
            url_validator(url)
        except ValidationError as e:
            error_message = str(e)

        if not error_message:
            if Bookmark.objects.filter(url=url).exists():
                error_message = "Закладка с таким URL уже существует."
            else:
                bookmark_data = parse_webpage(url)

                new_bookmark = Bookmark(url=url)
                if 'title' in bookmark_data:
                    new_bookmark.title = bookmark_data['title']
                if 'description' in bookmark_data:
                    new_bookmark.description = bookmark_data['description']
                if 'favicon' in bookmark_data:
                    new_bookmark.favicon = bookmark_data['favicon']
                new_bookmark.save()

    return render(
        request,
        'bookmarks/list_bookmarks.html',
        {'bookmarks': bookmarks},
    )


def parse_webpage(url):
    try:
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.660 YaBrowser/23.9.5.660 Yowser/2.5 Safari/537.36"
        }
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, "lxml")
            title = soup.find("title").text
            description = soup.find("meta", {'name': 'description'})
            if description:
                content = description.get('content')
            favicon = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
            if favicon:
                favicon = f'http://favicon.yandex.net/favicon/{url[8:]}'
                with open(f'{url[8:-1]}.jpg', 'wb') as file:
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
