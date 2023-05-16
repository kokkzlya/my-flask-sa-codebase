from flask import Blueprint, Flask, jsonify

from myproject.core.errors import BaseError
from . import auth, posts, users

bp = Blueprint("api", __name__, url_prefix="/api")


def register_blueprints(app: Flask):
    bp.register_blueprint(auth.bp, url_prefix="/auth")
    bp.register_blueprint(posts.bp, url_prefix="/posts")
    bp.register_blueprint(users.bp, url_prefix="/users")

    register_error_handlers(bp)

    app.register_blueprint(bp)


def register_error_handlers(bp: Blueprint):
    err_handlers = [
        (BaseError, handle_base_error, ),
        (401, handle_unauthorized_route, ),
        (404, handle_not_found_route, ),
    ]
    for h in err_handlers:
        bp.register_error_handler(h[0], h[1])


def handle_base_error(e):
    resp = jsonify(e.asdict())
    resp.headers.update(e.headers)
    return resp, e.status


def handle_unauthorized_route(e):
    return jsonify({
        'error': {
            'message': str(e),
            'status': 401,
            'type': "authorization_error",
        },
    }), 401


def handle_not_found_route(e):
    return jsonify({
        'error': {
            'message': str(e),
            'status': 404,
            'type': "not_found_error",
        },
    }), 404
