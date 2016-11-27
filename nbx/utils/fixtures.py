# -*- coding: utf-8 -*-

"""
    nbx.utils.fixtures
    ~~~~~~~~~~~~~~~~~~

    Module that implements some fixtures utilities.

    utilities based on Flask-Fixture extension,
    https://github.com/croach/Flask-Fixture

    :copyright: (c) 2016 by Augusto Roccasalva
    :license: GPLv3, see LICENSE for more details.
"""
import importlib

try:
    import yaml
except ImportError:
    def load(self, filename):
        raise Exception("Could not load fixture '{0}'. Make sure yo have "\
                        "PyYAML installed.".format(filename))

    yaml = type('FakeYaml', (object,), {
        'load': load,
    })()


def load_yaml(filename):
    with open(filename) as f:
        return yaml.load(f)


def load_fixtures(db, fixtures):
    """Loads the given fixtures into the database."""

    for fixture in fixtures:
        if 'model' in fixture:
            module_name, class_name = fixture['model'].rsplit('.', 1)
            module = importlib.import_module(module_name)
            model = getattr(module, class_name)
            for fields in fixture['records']:
                obj = model(**fields)
                db.session.add(obj)
            db.session.commit()
        elif 'table' in fixture:
            conn = db.engine.connect()
            table = db.Table(fixture['table'], db.metadata)
            conn.execute(table.insert(), fixture['records'])
        else:
            raise ValueError("Fixture missing a 'model' or 'table' field: {0}"\
                             .format(repr(fixture)))
