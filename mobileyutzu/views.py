# -*- coding: utf-8 -*-
from pyramid.url import route_url
from webob.exc import HTTPFound

from client import Client, TOOLS


def home(request):
    results = None
    q = ""
    if request.GET and "q" in request.GET:
        q = request.GET["q"]
        client = Client()
        results = client.search(q)
    return {'project': 'mobileyutzu',
            'title': "Mobile Yutzu",
            'subtitle': "Search a yutzu",
            'q': q,
            'results': results}


def document(request):
    # identifier = request.matchdict["id"]
    # lang = request.matchdict["lang"]
    # slug = request.matchdict["slug"]
    entity_url = route_url('entity', request, **request.matchdict)
    raise HTTPFound(location=entity_url)


def entity(request):
    identifier = request.matchdict["id"]
    back_url = None
    if request.GET and "q" in request.GET:
        back_url = "/?q=%s" % request.GET["q"]
    resources_url = route_url('resources', request, **request.matchdict)
    toc_url = route_url('toc', request, **request.matchdict)
    client = Client()
    entity = client.entity(identifier)
    if entity:
        title = entity["title"]
        document = entity["description"]
        subtitle = entity["id"]
        return {'project': 'mobileyutzu',
                'resources': resources_url,
                'toc': toc_url,
                'title': title,
                'subtitle': subtitle,
                'document': document,
                'back_url': back_url}
    else:
        raise HTTPFound(location='/')


def resources(request):
    return {'project': 'mobileyutzu'}


def toc(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    tools_dicts = [{
        "label": "Description",
        "value": client.entity()["description"],
        "url": route_url("entity", request, **request.matchdict),
    }]
    for tool_name in TOOLS:
        value = getattr(client, tool_name)()
        if value and value["objects"]:
            tools_dicts.append({
                "label": tool_name,
                "value": getattr(client, tool_name)(),
                "url": route_url(tool_name, request, **request.matchdict),
            })
    toc_url = route_url('toc', request, **request.matchdict)
    return {
        'project': 'mobileyutzu',
        'title': client.entity()["title"],
        'toc': toc_url,
        'tools': tools_dicts,
    }


def attachments(request):
    attachments_url = route_url("attachments", request, **request.matchdict)
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return {'project': 'mobileyutzu',
            'title': client.entity()["title"],
            'subtitle': identifier,
            'tool': "attachments",
            'document': client.attachments()}


def links(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return {'project': 'mobileyutzu',
            'title': client.entity()["title"],
            'subtitle': identifier,
            'tool': "links",
            'document': client.links()}


def pictures(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return {'project': 'mobileyutzu',
            'title': client.entity()["title"],
            'subtitle': identifier,
            'tool': "pictures",
            'document': client.pictures()}



def ypad(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return {'project': 'mobileyutzu',
            'title': client.entity()["title"],
            'subtitle': identifier,
            'tool': "ypad",
            'document': client.ypad()}



def social(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    social_objects = client.social()
    return {'project': 'mobileyutzu',
            'title': client.entity()["title"],
            'subtitle': identifier,
            'tool': "social",
            'document': client.social()}


def slides(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return {'project': 'mobileyutzu',
            'title': client.entity()["title"],
            'subtitle': identifier,
            'tool': "slides",
            'document': client.slides()}


def videos(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return {'project': 'mobileyutzu',
            'title': client.entity()["title"],
            'subtitle': identifier,
            'tool': "videos",
            'document': client.videos()}
