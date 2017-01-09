# -*- coding: utf-8 -*-

from functools import partial

from flask import current_app, make_response, json, request
from werkzeug.exceptions import HTTPException, InternalServerError
from werkzeug.http import HTTP_STATUS_CODES


class TonicException(Exception):
    werkzeug_exception = InternalServerError

    @property
    def status_code(self):
        return self.werkzeug_exception.code

    def as_dict(self):
        return {
            'stauts': self.status_code,
            'message': HTTP_STATUS_CODES.get(self.status_code, ''),
        }

    def get_response(self):
        response = jsonify(self.as_dict())
        response.status_code = self.status_code
        return response


def _make_response(data, code, headers=None):
    settings = {}
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', True)

    data = json.dumps(data, **settings)

    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    resp.headers['Content-Type'] = 'application/json'
    return resp


class Api(object):
    """
    This is the Tonic extension.
    """

    def __init__(self, app=None, prefix=None):
        self.app = app
        self.blueprint = None
        self.prefix = prefix or ''
        self.resources = {}
        self.views = []

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # If app is a blueprint, defer the initialization
        try:
            app.record(self._deferred_blueprint_init)
        except AttributeError:
            self._init_app(app)
        else:
            self.blueprint = app

    def _deferred_blueprint_init(self, setup_state):
        self.prefix = ''.join((setup_state.url_prefix or '', self.prefix))

        for resource in self.resources.values():
            resource.route_prefix = ''.join((self.prefix, '/', resource.meta.name))

        self._init_app(setup_state.app)

    def _init_app(self, app):
        app.config.setdefault('TONIC_MAX_PER_PAGE', 100)
        app.config.setdefault('TONIC_DEFAULT_PER_PAGE', 20)

        # Register schema endpoint
        #self._register_view(app,
        #                    rule=''.join((self.prefix, '/schema')),
        #                    view_func=self.output(self._schema_view),
        #                    endpoint='schema',
        #                    methods=['GET'])

        for route, resource, view_func, endpoint, methods in self.views:
            rule = route.rule_factory(resource)
            self._register_view(app, rule, view_func, endpoint, methods)

        app.handle_exception = partial(self._exception_handler, app.handle_exception)
        app.handle_user_exception = partial(self._exception_handler, app.handle_user_exception)

    def _register_view(self, app, rule, view_func, endpoint, methods):
        if self.blueprint:
            endpoint = '{}.{}'.format(self.blueprint.name, endpoint)

        app.add_url_rule(rule,
                         view_func=view_func,
                         endpoint=endpoint,
                         methods=methods)

    def _exception_handler(self, original_handler, e):
        if isinstance(e, TonicException):
            return e.get_response()

        if request.path.startswith(self.prefix):
            return original_handler(e)

        if isinstance(e, HTTPException):
            return _make_response({
                'status': e.code,
                'message': e.description,
            }, e.code)

        return original_handler(e)

    def add_resource(self, resource):
        """
        Add a :class:`Resource` class to the API and generate endpoints for all
        its routes.
        """
        # prevent resources from being added twice
        if resource in self.resources.values():
            return

        if resource.api is not None and resource.api != self:
            raise RuntimeError("Attempted to register a resource that is "
                               "already registered with a different Api.")

        # TODO: check or generates resources managers

        resource.api = self
        resource.route_prefix = ''.join((self.prefix, '/', resource.meta.name))

        for route in resource.routes.values():
            route_decorator = resource.meta.route_decorators.get(route.relation, None)
            self.add_route(route, resource, decorator=route_decorator)

        # TODO: inspect RouteSet attached to resource and add routes

        self.resources[resource.meta.name] = resource
