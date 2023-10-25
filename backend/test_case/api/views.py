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

    return render(request, 'list_bookmarks.html', {'bookmarks': context})
