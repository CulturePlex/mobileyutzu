import string
from random import sample, choice

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sqlalchemy import engine_from_config
from webob.exc import HTTPException

from client import TOOLS
from mobileyutzu.models import initialize_sql


def secret_key(length=128):
    chars = string.letters + string.digits
    return ''.join(choice(chars) for _ in xrange(length)) # way 4; 1.73 seconds


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig(secret_key())
    # configuration setup
    config = Configurator(settings=settings, session_factory=session_factory)
    # routes setup
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'mobileyutzu:static')
    config.add_route('home', '/',
                     view='mobileyutzu.views.home',
                     view_renderer='templates/home.jinja2')
    config.add_route('document', '{lang}/{id}/{slug}/',
                     view='mobileyutzu.views.document',
                     view_renderer='templates/document.jinja2')
    config.add_route('entity', '{id}/',
                     view='mobileyutzu.views.entity',
                     view_renderer='templates/document.jinja2')
    config.add_route('resources', '{id}/resources/',
                     view='mobileyutzu.views.resources',
                     view_renderer='templates/resources.jinja2')
    config.add_route('toc', '{id}/toc/',
                     view='mobileyutzu.views.toc',
                     view_renderer='templates/toc.jinja2')
    tools = ["attachments", "links", "pictures", "ypad", "social", "slides",
             "videos"]
    for tool in TOOLS:
        config.add_route(tool, '{id}/%s/' % tool,
                         view='mobileyutzu.views.%s' % tool,
                         view_renderer='templates/tool.jinja2')
    config.add_view(error_view, context=HTTPException)
    return config.make_wsgi_app()

def error_view(context, request):
    return context
