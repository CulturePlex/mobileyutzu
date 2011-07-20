# -*- coding: utf-8 -*-
from pyramid.url import route_url
from webob.exc import HTTPFound

from client import Client
from utils import get_tools, request_context


def home(request):
    results = None
    q = request.session.get("q", "")
    if q or (request.GET and "q" in request.GET):
        q = request.GET.get("q", "") or q
        client = Client()
        results = client.search(q.encode("utf8"))
        if results:
            request.session.update({"q": q})
    return {'project': 'mobileyutzu',
            'title': "Mobile Yutzu",
            'subtitle': "Search a yutzu",
            'q': q,
            'results': results}


def document(request):
    entity_url = route_url('entity', request, **request.matchdict)
    raise HTTPFound(location=entity_url)


def entity(request):
    identifier = request.matchdict["id"]
    resources_url = route_url('resources', request, **request.matchdict)
    toc_url = route_url('toc', request, **request.matchdict)
    client = Client(identifier)
    entity = client.entity()
    if entity:
        tools_dicts = get_tools(request, client)
        title = entity["title"]
        document = entity["description"]
        subtitle = entity["id"]
        return {'project': 'mobileyutzu',
                'resources': resources_url,
                'toc': toc_url,
                'title': title,
                'subtitle': subtitle,
                'tools': tools_dicts,
                'document': document}
    else:
        raise HTTPFound(location='/')


def resources(request):
    resources_url = route_url('resources', request, **request.matchdict)
    toc_url = route_url('toc', request, **request.matchdict)
    return {
        'project': 'mobileyutzu',
        'resources': resources_url,
        'toc': toc_url,
    }


def toc(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    tools_dicts = get_tools(request, client, value=True)
    resources_url = route_url('resources', request, **request.matchdict)
    toc_url = route_url('toc', request, **request.matchdict)
    return {'project': 'mobileyutzu',
            'title': client.entity()["title"],
            'toc': toc_url,
            'resources': resources_url,
            'tools': tools_dicts}


def description(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return request_context(request, client, {
            'tool': "description",
            'document': client.description()
    })


def attachments(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return request_context(request, client, {
            'tool': "attachments",
            'document': client.attachments()
    })


def links(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return request_context(request, client, {
            'tool': "links",
            'document': client.links()
    })


def pictures(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return request_context(request, client, {
            'tool': "pictures",
            'document': client.pictures()
    })


def ypad(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return request_context(request, client, {
            'tool': "ypad",
            'document': client.ypad()
    })


def social(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return request_context(request, client, {
            'tool': "social",
            'document': client.social()
    })


def slides(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return request_context(request, client, {
            'tool': "slides",
            'document': client.slides()
    })


def videos(request):
    identifier = request.matchdict["id"]
    client = Client(identifier)
    return request_context(request, client, {
            'tool': "videos",
            'document': client.videos()
    })
