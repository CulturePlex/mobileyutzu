# -*- coding: utf-8 -*-
import json
from urllib import quote_plus

from request import Request

PROVIDER_URL = "http://www.yutzu.com"
TOOLS = ["attachments", "links", "pictures", "ypad", "social", "slides",
         "videos"]


class Client(object):

    def __init__(self, identifier="", provider=None):
        self.provider = provider or PROVIDER_URL
        self.identifier = identifier
        self._entity = "/api/v1/entity/%s/?format=json"
        self._attachments = "/api/v1/attachment/?format=json&entity=%s"
        self._links = "/api/v1/links/?format=json&entity=%s"
        self._pictures = "/api/v1/pictures/?format=json&entity=%s"
        self._ypad = "/api/v1/ypad/?format=json&entity=%s"
        self._social = "/api/v1/social/?format=json&entity=%s"
        self._slides = "/api/v1/slides/?format=json&entity=%s"
        self._videos = "/api/v1/videos/?format=json&entity=%s"
        self._search = "/api/v1/entity/?format=json&title=%s"
        self._objects = "/api/v1/%s/%s/"
        # self._objects = "/api/v1/%s/?format=json&entity=%s"
        self._twitter = "http://search.twitter.com/search.json?q=%s"

    def _get(self, url=None, absolute_url=False):
        if url:
            if absolute_url:
                response = Request().get(url)
            else:
                response = Request().get("%s/%s" % (self.provider, url))
        else:
            response = Request().get("%s" % self.provider)
        if isinstance(response, (tuple, list)):
            if len(response) > 0:
                if "status" in response[0]:
                    if response[0]["status"] == '200':
                        return json.loads(response[1])
        return None

    def entity(self, identifier=None):
        return self._get(self._entity % (identifier or self.identifier))

    def attachments(self, identifier=None):
        return self._get(self._attachments % (identifier or self.identifier))

    def links(self, identifier=None):
        return self._get(self._links % (identifier or self.identifier))

    def pictures(self, identifier=None):
        response = self._get(self._pictures % (identifier or self.identifier))
        pictures_items = {"objects": []}
        if "objects" in response and response["objects"]:
            for obj in response["objects"]:
                images_object = json.loads(obj["images_object"])
                for image in images_object:
                    for attr in ["src", "thumbnail_src"]:
                        if (attr in image
                            and not image[attr].startswith(PROVIDER_URL)):
                            image[attr] = u"%s%s" % (PROVIDER_URL, image[attr])
                    pictures_items["objects"].append(image)
        return pictures_items

    def ypad(self, identifier=None):
        return self._get(self._ypad % (identifier or self.identifier))

    def social(self, identifier=None):
        response = self._get(self._social % (identifier or self.identifier))
        social_items = {"objects": []}
        if "objects" in response and response["objects"]:
            for obj in response["objects"]:
                keyword = obj["keyword"]
                twitter_messages = self._get(self._twitter % keyword, True)
                social_items["objects"].append(twitter_messages)
        return social_items

    def slides(self, identifier=None):
        return self._get(self._slides % (identifier or self.identifier))

    def videos(self, identifier=None):
        return self._get(self._videos % (identifier or self.identifier))

    def objects(self, object_type, identifier):
        if object_type in TOOLS:
            return self._get(self._objects % (object_type, identifier))
        return None

    def search(self, query, limit=0, offset=0):
        search_url = self._search % quote_plus(query)
        if limit:
            search_url = "%s&limit=%s" % limit
        if offset:
            search_url = "%s&offset=%s" % offset
        return self._get(search_url)
