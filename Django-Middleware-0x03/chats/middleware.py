# chats/middleware.py
import logging
from datetime import datetime, timedelta
import time
from django.utils import timezone
import os
from django.http import HttpResponseForbidden
from collections import defaultdict, deque


class RolepermissionMiddleware:
    """
    Sanitise action with Role base Middleware
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.restricted_paths = ["/admin"]
        logging.info(
            f"[{datetime.now()}] RolepermissionMiddleware  initialized. Restricted paths: {self.restricted_paths}"
        )

    def __call__(self, request):
        # check request path is restricted
        for path_prefix in self.restricted_paths:
            logging.warning(
                f"[{datetime.now()}] RolepermissionMiddleware path_prefix: {path_prefix}"
            )
            if request.path.startswith(path_prefix):
                if not (
                    request.user.is_authenticated
                    and (request.user.is_staff or request.user.is_superuser)
                ):
                    logging.warning(
                        f"[{datetime.now()}] RolepermissionMiddleware request path: {request.path}"
                    )
                    logging.warning(
                        f"[{datetime.now()}] RolepermissionMiddleware request user staff: {request.user.is_staff}"
                    )
                    logging.warning(f"[{datetime.now()}] RolepermissionMiddleware request user is_staff: {request.user}")

                    user_info = (
                        request.user.first_name
                        if request.user.is_authenticated
                        else "AnonymousUser"
                    )
                    logging.warning(
                        f"[{datetime.now()}] Access denied for User: {user_info} - "
                        f"{request.path} - requires admin role/moderator privileges"
                    )
                    return HttpResponseForbidden(
                        "Access denied, you do not have permission to access this resource"
                    )

        # proceed request if not restricted
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Track messages and limit number of message per ip
    """

    # store request stamps for each Ip address
    IP_REQUEST_TIMESTAMPS = defaultdict(deque)

    # configure rate limiting
    RATE_LIMIT_MESSAGES = 5  # mssages per window
    RATE_LIMIT_WINDOW_SECONDS = 60  # in time seconds

    def __init__(self, get_response):
        self.get_response = get_response
        logging.info(
            f"[{datetime.now()}] OffensiveLanguageMiddleware initialized. Rate limit: {self.RATE_LIMIT_MESSAGES} messages per {self.RATE_LIMIT_WINDOW_SECONDS} seconds."
        )

    def __call__(self, request):
        # get user IP address
        # use X-Forwarded-For if behind a proxy otherwise REMOTE_ADDR
        ip_address = request.META.get("X-Forwarded-For")
        if ip_address:
            # consideration, if X-forwarded-for is a list pick the first
            ip_address = ip_address.split(",")[0].strip()
        else:
            ip_address = request.META.get("REMOTE_ADDR")
        response = self.get_response(request)
        if request.method == "POST":
            current_time = datetime.now()

            # get the daque of timestamp for ip
            timestamps = self.IP_REQUEST_TIMESTAMPS[ip_address]

            # Remove timestamps that are outside the time window
            # Iterate from the left (oldest) and remove if too old
            while timestamps and timestamps[0] < current_time - timedelta(
                seconds=self.RATE_LIMIT_WINDOW_SECONDS
            ):
                timestamps.popleft()

            # check if current request would exceed the limit
            if len(timestamps) >= self.RATE_LIMIT_MESSAGES:
                user = (
                    request.user if request.user.is_authenticated else "AnonymousUser"
                )
                logging.info(
                    f"[{datetime.now()}] Rate limit exceeded for IP: {ip_address} (User: {user}) - "
                    f"Path: {request.path}. Limit: {self.RATE_LIMIT_MESSAGES} messages per {self.RATE_LIMIT_WINDOW_SECONDS}s."
                )

                return HttpResponseForbidden(
                    f"You have exceeded the message rate limit of {self.RATE_LIMIT_MESSAGES} messages per minute. Please try again later."
                )
            # add current time to the daque for tracking
            timestamps.append(current_time)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the messaging app during certain hours of the day.
    Denies access with a 403 Forbidden error if the current server time is outside
    9 AM (09:00) and 6 PM (18:00).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.start_hour = 9  # 9 AM
        self.end_hour = 18  # 6PM
        logging.info(
            f"[{datetime.now()}] RestrictAccessByTimeMiddleware initialized."
            f"Access allowed between {self.start_hour}:00 and {self.end_hour}:00."
        )

    def __call__(self, request):
        current_hour = datetime.now().hour

        # check current hour
        if not (self.start_hour <= current_hour < self.end_hour):
            # deny access
            logging.warning(f"[{datetime.now}] access denied path: {request.path} ")
            return HttpResponseForbidden(
                "Access to the messaging app is restricted outside of 9 AM and 6 PM."
            )

        # proceed request if outside restricted time
        response = self.get_response(request)
        return response


# configure request logger
logger = logging.getLogger("request_logger")

# create path if it does not exist
log_path = ""
# if not os.path.exists(log_path):
# os.makedirs(log_path)

log_file_path = os.path.join(log_path, "requests.log")

# create a file handler for the logger
# logging mode "a" apend new lines to end of file
log_file_handler = logging.FileHandler(log_file_path, "a")

# define message format
formatter = logging.Formatter("%(message)s")
log_file_handler.setFormatter(formatter)

# add logger handlers, prevent multiple handlers if request is already loaded
if not logger.handlers:
    logger.addHandler(log_file_handler)
    logger.setLevel(logging.INFO)  # set logger level


class RequestLoggingMiddleware:
    """
    Middleware to log user requests to file
    """

    def __init__(self, get_response):
        """
        Logger initialise
        """
        self.get_response = get_response
        logger.info(f"[{datetime.now()}] RequestLoggingMiddleware initialised")

    def __call__(self, request):
        """
        Execute before request
        """

        # execution start
        start_time = time.time()

        # call view
        response = self.get_response(request)

        # comletion time
        end_time = time.time()

        # duration
        exec_time = end_time - start_time

        self.process_response(request, response, exec_time)

        return response

    def process_response(self, request, response, exec_time):
        """
        Process response after view has been executed
        """

        # request user
        self.user = request.user
        # log the request information
        log_message = f"{datetime.now()} - User: {self.user} - Path: {request.path}"
        # log message to file
        logger.info(log_message)

        if hasattr(request, "user") and request.user.is_authenticated:
            user_info = request.user
        else:
            user_info = "Anon"

        # log request complete
        log_reponse = f"{datetime.now()} - Execution time {exec_time:.2f} seconds, User - {user_info}"
        logger.info(log_reponse)
