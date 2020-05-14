# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from flask import url_for, Blueprint, render_template, Response


class Apidoc(Blueprint):
    '''
    Allow to know if the blueprint has already been registered
    until https://github.com/mitsuhiko/flask/pull/1301 is merged
    '''
    def __init__(self, *args, **kwargs):
        self.registered = False
        super(Apidoc, self).__init__(*args, **kwargs)

    def register(self, *args, **kwargs):
        super(Apidoc, self).register(*args, **kwargs)
        self.registered = True


apidoc = Apidoc('restplus_doc', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/swaggerui',
)


@apidoc.add_app_template_global
def swagger_static(filename):
    return url_for('restplus_doc.static', filename=filename)


def ui_for(api):
    '''Render a SwaggerUI for a given API'''
    if api._hide_specs_url:
        return render_template('swagger-ui.html', title=api.title,
        specs_json=api.__schema__, specs_url=None)
    return render_template('swagger-ui.html', title=api.title,
                           specs_url=api.specs_url)


def specs_for(api):
    swagger_specs = json.dumps(api.__schema__, sort_keys=True, indent=4, separators=(',', ': '))
    return Response(swagger_specs, mimetype='application/json')
