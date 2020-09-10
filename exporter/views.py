from django.shortcuts import render
from .models import Entry
from os import path
from django.http import HttpResponse


def index(request, **kwargs):
    return render(request, "index.html.j2", {'title': 'MyTitle', 'text': "MyText"})

def export(request, **kwargs):
    filename, ext = path.splitext(request.path[1:])
    try:
        entry = Entry.objects.get(content=filename)
    except:
        return HttpResponse("ERROR: No such object", content_type="text/plain")
    if ext == '.json':
        return HttpResponse(entry.to_json(), content_type="application/json")
    elif ext == '.yaml':
        return HttpResponse(entry.to_yaml(), content_type="text/yaml")
    elif ext == '.toml':
        return HttpResponse(entry.to_toml(), content_type="text/plain")
    elif ext == '.conf':
        return HttpResponse(entry.to_nginx(), content_type="text/plain")
    else:
        return HttpResponse(f"Unknown extension: {ext}", content_type="text/plain")
