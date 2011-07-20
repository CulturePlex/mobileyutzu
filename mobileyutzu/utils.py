# -*- coding: utf-8 -*-
from pyramid.url import route_url

from client import TOOLS


def request_context(request, client, dic={}):
    identifier = request.matchdict["id"]
    tools_dicts = get_tools(request, client)
    resources_url = route_url('resources', request, **request.matchdict)
    toc_url = route_url('toc', request, **request.matchdict)
    result = {
            'project': 'mobileyutzu',
            'resources': resources_url,
            'toc': toc_url,
            'title': client.entity()["title"],
            'subtitle': identifier,
            'tools': tools_dicts,
    }
    result.update(dic)
    return result


def get_tools(request, client, value=False):
    if value:
        tools_dicts = [{
            "label": "Description",
            "value": client.entity()["description"],
            "url": route_url("entity", request, **request.matchdict),
        }]
    else:
        tools_dicts = [{
            "label": "Description",
            "url": route_url("entity", request, **request.matchdict),
        }]
    for tool_name in TOOLS:
        tool_value = getattr(client, tool_name)()
        if tool_value and tool_value["objects"]:
            if value:
                tools_dicts.append({
                    "label": tool_name,
                    "value": tool_value,
                    "url": route_url(tool_name, request, **request.matchdict),
                })
            else:
                tools_dicts.append({
                        "label": tool_name,
                        "url": route_url(tool_name, request, **request.matchdict),
                    })
    return tools_dicts
