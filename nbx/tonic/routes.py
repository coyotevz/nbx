# -*- coding: utf-8 -*-

"""
    tonic.routes
    ~~~~~~~~~~~~

    Tools that build routes for resources.
"""

from types import MethodType

HTTP_METHODS = ('GET', 'PUT', 'POST', 'PATCH', 'DELETE')
HTTP_METHOD_VERB_DEFAULTS = {
    'GET': 'read',
    'PUT': 'create',
    'POST': 'create',
    'PATCH': 'update',
    'DELETE': 'destroy',
}

def _method_decorator(method):
    def wrapper(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return self.for_method(method, args[0], **kwargs)
        else:
            return lambda f: self.for_method(method, f, *args, **kwargs)
    wrapper.__name__ = method
    return wrapper


class Route(object):
    """
    Decorator to build route
    """

    def __init__(self,
                 method=None,
                 view_func=None,
                 rule=None,
                 attribute=None,
                 rel=None,
                 title=None,
                 description=None,
                 schema=None,
                 response_schema=None,
                 format_response=None):

        self.rel = rel
        self.rule = rule
        self.method = method
        self.attribute = attribute
        self.title = title
        self.description = description

        self.view_func = view_func
        self.format_response = format_response

        annotations = getattr(view_func, '__annotations__', None)

        if isinstance(annotations, dict) and len(annotations):
            self.request_schema = {name: field for name, field in annotations.items() if name != 'return'}
            self.response_schema = annotations.get('return', response_schema)
        else:
            self.request_schema = schema
            self.response_schema = response_schema

        for method in HTTP_METHODS:
            setattr(self, method, MethodType(_method_decorator(method), self))

    def for_method(self, method, view_func, rel=None, title=None, description=None, schema=None, response_schema=None, **kwargs):

        attribute = kwargs.pop('attribute', self.attribute)
        format_response = kwargs.pop('format_response', self.format_response)


def _route_decorator(method):
    @classmethod
    def decorator(cls, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return cls(method, args[0])
        else:
            return lambda f: cls(method, f, *args, **kwargs)

    if sys.version_info.major > 2:
        decorator.__name__ = method
    return decorator

for method in HTTP_METHODS:
    setattr(Route, method, _route_decorator(method))
