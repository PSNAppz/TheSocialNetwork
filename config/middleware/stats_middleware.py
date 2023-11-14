import time
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class StatsMiddleware(MiddlewareMixin):
    """ 
    This middleware calculates request response time. 
    The stats is then displayed along the log-output,
    if DEBUG is set to True.
    """

    def process_request(self, request):
        "Start time at request coming in"
        if settings.DEBUG:
            request.start_time = time.time()
            request.request_in_time = datetime.strftime(
                timezone.localtime(timezone.now()),
                '%d/%m/%Y %I:%M:%S %p'
            )
            print(
                "[REQUEST]:", "IN",
                " [API EndPoint]:", request.path,
                " [Request In Time]:", request.request_in_time
            )

    def process_response(self, request, response):
        "End of request, take time"
        if settings.DEBUG:
            total = time.time() - request.start_time
            try:
                display_name = request.user.display_name
            except:
                display_name = None
            print(
                "[User]:", display_name,
                " [API EndPoint]:", request.path,
                " [Request In Time]:", request.request_in_time,
                " [Time]:", int(total * 1000), "ms"
            )
        return response

