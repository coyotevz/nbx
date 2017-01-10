# -*- coding: utf-8 -*-

import six

from .utils import AttributeDict

class ResourceMeta(type):

    def __new__(mcs, name, bases, members):
        class_ = super(ResourceMeta, mcs).__new__(mcs, name, bases, members)
        class_.routes = routes = dict(getattr(class_, 'routes') or {})
        class_.meta = meta = AttributeDict(getattr(class_, 'meta', {}) or {})

        if 'Meta' in members:
            changes = members['Meta'].__dict__
            for k, v in changes.items():
                if not k.startswith('__'):
                    meta[k] = v

            if not changes.get('name', None):
                meta['name'] = name.lower()
        else:
            meta['name'] = name.lower()

        schema = {}
        for base in bases:
            if hasattr(base, 'Schema'):
                schema.update(base.Schema.__dict__)

        if 'Schema' in members:
            schema.update(members['Schema'].__dict__)

        if schema:
            class_.schema = fs = \
                {k: f for k, f in schema.items() if not k.startswith('__')}#,
                #required_fields=meta.get('required_fields', None)

        return class_


class Resource(six.with_metaclass(ResourceMeta, object)):
    """
    A plain resource with nothing but a schema.
    """
    api = None
    meta = None
    routes = None
    schema = None
    route_prefix = None

    class Meta:
        name = None
        title = None
        description = None
        required_fields = None
        exclude_routes = ()
        route_decorators = {}
        read_only_fields = ()
        write_only_fields = ()
        paginated = True


class ModelResourceMeta(ResourceMeta):

    def __new__(mcs, name, bases, members):
        class_ = super(ModelResourceMeta, mcs).__new__(mcs, name, bases, members)

        if 'Meta' in members:
            meta = class_.meta
            changes = members['Meta'].__dict__

            # TODO: create a manager or thin layer to store

        return class_


class ModelResource(six.with_metaclass(ModelResourceMeta, Resource)):

    manager = None

    class Schema:
        pass

    class Meta:
        id_attribute = None     # use 'id' by default
        sort_attribute = None   # None means use id_attribute
        id_converter = None
        manager = None
        include_fields = None
        exclude_fields = None
        filters = True

