import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import make_response, jsonify
from flask_limiter import Limiter, RequestLimit
from datetime import datetime
import zoneinfo


# Limiter object
limiter = Limiter(
    get_remote_address,
    storage_uri=os.getenv("REDIS_URI"),
    storage_options={"socket_connect_timeout": 30},
    strategy="fixed-window",
)


class LimiterService:
    """LimiterService

    Object used for communication between app and redis database.

    In app it is used to declare limit number of possible requests by the usee (per IP).
    Information is send and downloaded from redis cloud instance.
    """

    def __init__(self, app=None):

        self.limiter = limiter

        self.limiter._on_breach = self.default_error_responder

    def init_app(self, app):
        """
        Initialize app for limiter
        """

        self.limiter.init_app(app)

    def default_error_responder(self, request_limit: RequestLimit):
        """
        Default error responder (429) for too many request errorr

        Args:
            request_limit (RequestLimit): current ip limit

        Returns:
            Response: response for site with information about reset time.
        """
        reset_at = datetime.fromtimestamp(
            request_limit.reset_at, tz=zoneinfo.ZoneInfo("Europe/Warsaw")
        )
        print(f"reset_at: {reset_at}")
        return make_response(
            jsonify({"reset_at": reset_at.strftime("%H:%M %Y-%m-%d")}), 429
        )
