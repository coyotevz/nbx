# -*- coding: utf-8 -*-

from marshmallow.compat import with_metaclass
from marshmallow_sqlalchemy import ModelSchema

def _create_model_schema(schema_opts, meta_opts):

    # is common pattern that resources name ends with 'Resource' word
    name = meta_opts['name'].replace('Resource', '') + 'Schema'
    meta = type('Meta', (object,), {'model': meta_opts['model']})
    ns = {"Meta": meta}
    ns.update(schema_opts)
    schema = type(name, (ModelSchema,), ns)
    return schema


class ResourceMeta(type):

    def __new__(cls, name, bases, namespace):
        new_cls = super(ResourceMeta, cls).__new__(cls, name, bases, namespace)

        routes = dict(getattr(new_cls, 'routes', {}) or {})
        meta_opts = {}
        schema_opts = {}

        for base in bases:
            # TODO: add routes from base

            # FIXME: is this necessary if we are using meta_opts from new_cls??
            meta_opts.update(getattr(base, 'meta_opts', {}) or {})
            schema_opts.update(getattr(base, 'schema_opts', {}) or {})

        if 'Meta' in namespace:
            opts = namespace['Meta'].__dict__
            meta_opts.update({k: v for k, v in opts.items()
                              if not k.startswith('__')})

            if not opts.get('name', None):
                meta_opts['name'] = name
        else:
            meta_opts['name'] = name

        if 'Schema' in namespace:
            opts = namespace['Schema'].__dict__
            schema_opts.update({k: v for k, v in opts.items()
                                if not k.startswith('__')})

        new_cls.routes = routes
        new_cls.meta_opts = meta_opts
        new_cls.schema_opts = schema_opts

        if getattr(meta_opts, "model", None) is not None:
            new_cls.schema_class = _create_model_schema(schema_opts, meta_opts)
        else:
            # TODO: create a normal ma schema
            new_cls.schema_class = '<noset>'

        # TODO: add routes from namespace

        return new_cls



class Resource(with_metaclass(ResourceMeta, object)):

    api = None
    route_prefix = None

    class Meta:
        name = None
        title = None
        description = None
        exclude_routes = ()
        route_decorators = {}

        model = None
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
