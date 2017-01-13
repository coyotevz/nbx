# -*- coding: utf-8 -*-


from marshmallow.compat import with_metaclass
from marshmallow import Schema
from marshmallow_sqlalchemy import ModelSchema

SCHEMA_OPTIONS = [
    # marshmallow
    'fields',
    'additional',
    'include',
    'exclude',
    'dateformat',
    'strict',
    'json_module',
    'ordered',
    'index_error',
    'load_only',
    'dump_only',

    # marshmallow-sqlalchemy
    'model',
    'sqla_session',
    'model_converter',
    'include_fk',
]

def _extract_schema_options(meta_opts):
    # Modify meta_opts
    opts = {}
    for o in SCHEMA_OPTIONS:
        if o in meta_opts:
            opts[o] = meta_opts.pop(o)
    return opts

def _create_schema(name, schema_decl, schema_opts):

    if schema_opts.get("model", None):
        Base = ModelSchema
    else:
        Base = Schema

    ns = {"Meta": type('Meta', (object,), schema_opts)}
    ns.update(schema_decl)
    schema = type(name, (Base,), ns)
    return schema


class ResourceMeta(type):

    def __new__(cls, name, bases, namespace):
        new_cls = super(ResourceMeta, cls).__new__(cls, name, bases, namespace)

        routes = dict(getattr(new_cls, 'routes', {}) or {})
        meta_opts = {}
        schema_opts = {}    # Schema optons as marshmallow uses
        schema_decls = {}   # Schema fields as marshmallow uses

        for base in bases:
            # TODO: add routes from base
            meta_opts.update(getattr(base, 'meta_opts', {}) or {})
            schema_opts.update(getattr(base, 'schema_opts', {}) or {})
            schema_decls.update(getattr(base, 'schema_decls', {}) or {})

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
            schema_decls.update({k: v for k, v in opts.items()
                                if not k.startswith('__')})

        schema_opts.update(_extract_schema_options(meta_opts))

        new_cls.routes = routes
        new_cls.meta_opts = meta_opts
        new_cls.schema_opts = schema_opts
        new_cls.schema_decls = schema_decls

        new_cls.schema_class = _create_schema(name+'Schema',
                                              schema_decls,
                                              schema_opts)

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
        filters = True

    class Schema:
        pass
