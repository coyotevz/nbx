# -*- coding: utf-8 -*-

import six

from utils import AttributeDict


class ResourceMeta(type):

    def __new__(cls, name, bases, namespace):
        new_cls = super(ResourceMeta, cls).__new__(cls, name, bases, namespace)

        routes = dict(getattr(new_cls, 'routes') or {})
        meta = AttributeDict(getattr(new_cls, 'meta', {}) or {})
        schema = {}

        for base in bases:
            # TODO: add routes from base

            if hasattr(base, 'Meta'):
                meta.update({k: v for k, v in base.Meta.__dict__.items()
                             if not k.startswith('__')})
            if hasattr(base, 'Schema'):
                schema.update(base.Schema.__dict__)

        if 'Meta' in namespace:
            options = namespace['Meta'].__dict__
            meta.update({k: v for k, v in options.items()
                         if not k.startswith('__')})

            if not options.get('name', None):
                meta['name'] = name.lower()
        else:
            meta['name'] = name.lower()

        if 'Schema' in namespace:
            schema.update(namespace['Schema'].__dict__)

        new_cls.routes = routes
        new_cls.meta = meta
        new_cls.schema = schema

        # TODO: add routes from namespace

        return new_cls



class Resource(six.with_metaclass(ResourceMeta, object)):

    api = None
    meta = None
    routes = None
    schema = None
    route_prefix = None

    class Meta:
        name = None
        title = None
        description = None
        exclude_routes = ()
        route_decorators = {}

        id_attribute = None         # user 'id' by default
        sort_attribute = None       # None means use id_attribute
        id_converter = None
        include_id = True
        include_type = False
        include_fields = None
        exclude_fields = None
        filters = True

    class Schema:
        pass
