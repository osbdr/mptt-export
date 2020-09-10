from django.shortcuts import render
from .models import Entry
from os import path
from django.http import HttpResponse


def index(request, **kwargs):
    return render(request, "index.html.j2", {'title': 'MyTitle', 'text': "MyText"})

def export(request, **kwargs):
    filename, ext = path.splitext(request.path[1:])
    print(filename, ext)
    try:
        #entry = list(filter(lambda x: x.content == filename and x.is_root_node(), Entry.objects.all()))
        #assert len(entry) == 1, f"No such element: {filename}"
        #entry = entry[0]
        entry = Entry.objects.get(content=filename,parent=None) #.filter(parent__isnull=True)
    except Exception as e:
        return HttpResponse(e, content_type="text/plain")
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
