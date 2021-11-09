from django.shortcuts import render
from .settings import handlers
import asyncio


async def new_view(request):
    list_handlers = [handler for key, handler in handlers.items()]
    list_context = await asyncio.gather(*list_handlers, return_exceptions=True)
    print('^^^^^^^^^^list_context', list_context)
    context = dict()
    for index, key in enumerate(handlers):
        context[key] = list_context[index]

    print('^^^^^^^^^^context', context)

    return render(request, 'news/news.html', context)



