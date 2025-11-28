#!/usr/bin/env python3

"""
Main Flask application setup for the Pharmacy API.
"""

# from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask, abort, request, g, Response
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from typing import Any
import logging
import os
import sys
import traceback

from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.utils.error_handlers import (
    bad_request, unauthorized, forbidden, not_found, method_not_allowed,
    conflict_error, server_error
)
from api.v1.views import app_views
from models import storage


load_dotenv()
logger = logging.getLogger(__name__)
bcrypt = Bcrypt()
auth = SessionDBAuth()


ALLOWED_ORIGINS = [
            "https://pharmacy-inventory-app.vercel.app",
            "http://localhost:5173"
        ]

def check_authentication():
    """
    Verifies session authentication for protected routes.
    """
    if request.method == 'OPTIONS':
        return  # Allow the OPTIONS request to proceed unauthenticated
    
    if not auth.require_auth(
        request.path,
        [
            "/api/v1/register/", "/api/v1/auth_session/login/"
        ]
    ):
        return
    if not auth.session_cookie():
        abort(401)
    
    employee = auth.current_employee()
    if not employee:
        abort(401)
    g.current_employee = employee

def close_db(exception: BaseException | None) -> None:
    """
    Closes the database session after each request.
    """
    storage.close()

def create_app(config_name: str | None=None) -> Flask:
    """
    Creates and configures the Flask application instance.
    """
    app = Flask(__name__)

    if config_name == "test":
        app.config.from_mapping(TESTING=True)
    else:
        app.config.from_mapping(TESTING=False)

    bcrypt.init_app(app) # type: ignore
    CORS(
        app,
        resources={r"/api/v1/*": {
            "origins": ["http://localhost:5173", "https://pharmacy-inventory-app.onrender.com"]
        }},
        allow_headers=["Content-Type", "Authorization", "X-Custom-Header"],
        supports_credentials=True
    )
    app.register_blueprint(app_views)
    app.before_request(check_authentication)
    app.teardown_appcontext(close_db)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(409, conflict_error)
    app.register_error_handler(500, server_error)

    # from api.v1.utils.utility import run_monthly_reordering_point_update

    # scheduler = BackgroundScheduler()
    
    # # Run at 00:00 on the first day of every month
    # scheduler.add_job( # type: ignore
    #     run_monthly_reordering_point_update,
    #     'cron', day=1, hour=0, minute=0
    # )

    # scheduler.start() # type: ignore

    # for rule in app.url_map.iter_rules():
    #     print(rule.endpoint, rule.methods, rule.rule)

    @app.errorhandler(500)
    def handle_internal_server_error(e: Any): # type: ignore
        # This forces the full traceback to print to the console
        traceback.print_exc(file=sys.stderr)

        # Return a generic response to the browser
        return "An internal server error occurred. Check server logs for details.", 500

    @app.after_request
    def force_cors_headers(response: Response): # type: ignore
        # 1. Get the origin from the request headers
        origin = request.headers.get('Origin')

        # 2. Check if the requesting origin is in our allowed list
        if origin and origin in ALLOWED_ORIGINS:
            # 3. CRITICAL: Set the mandatory credentialed CORS headers
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'

        return response
    
    return app


config_name = os.getenv("FLASK_ENV", "development")
app = create_app(config_name)

if __name__ == "__main__":
    host = os.getenv("PHARMACY_API_HOST", "0.0.0.0")
    port = int(os.getenv("PHARMACY_API_PORT", 5000))
    FLASK_DEBUG = bool(int(os.getenv("FLASK_DEBUG", 0)))
    app.run(host=host, port=port, threaded=True, debug=FLASK_DEBUG)
    