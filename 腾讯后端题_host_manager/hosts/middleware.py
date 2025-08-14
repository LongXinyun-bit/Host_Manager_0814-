import time
from django.utils.deprecation import MiddlewareMixin


class RequestTimingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._start_time = time.perf_counter()

    def process_response(self, request, response):
        try:
            cost_ms = (time.perf_counter() - getattr(request, '_start_time', time.perf_counter())) * 1000
            response['X-Request-Time-ms'] = f"{cost_ms:.2f}"
        except Exception:
            pass
        return response 