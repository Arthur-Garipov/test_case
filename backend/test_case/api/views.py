from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import render

from .models import Bookmark
from .utils import parse_webpage


def list_bookmarks(request):
    bookmarks = Bookmark.objects.all()
    context = []

    for bookmark in bookmarks:
        parsed_data = parse_webpage(bookmark.url)
        if 'error' not in parsed_data:
            title = parsed_data['title']
            description = parsed_data['description']
            favicon = parsed_data['favicon']
        else:
            title = bookmark.url
            description = ""
            favicon = ""

        context.append(
            {
                'title': title,
                'url': bookmark.url,
                'description': description,
                'favicon': favicon,
            }
        )

    return render(
        request, 'bookmarks/list_bookmarks.html', {'bookmarks': context}
    )


def add_bookmark(request):
    error_message = None

    if request.method == 'POST':
        url = request.POST.get('url')

        url_validator = URLValidator()
        try:
            url_validator(url)
        except ValidationError as e:
            error_message = str(e)

        if not error_message:
            if Bookmark.objects.filter(url=url).exists():
                error_message = "Закладка с таким URL уже существует."
            else:
                new_bookmark = Bookmark(url=url)
                new_bookmark.save()

    return render(
        request,
        'bookmarks/add_bookmark.html',
        {'error_message': error_message},
    )
