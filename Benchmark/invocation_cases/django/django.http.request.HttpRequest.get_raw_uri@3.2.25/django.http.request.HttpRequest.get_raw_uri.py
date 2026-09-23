import django
from django.conf import settings
from django.http import HttpRequest
import inspect

def main():
    # Configure Django settings
    settings.configure(DEFAULT_CHARSET='utf-8')

    # Simulate a request
    request = HttpRequest()
    request.path = '/test/'
    request.META['HTTP_HOST'] = 'example.com'
    request.META['wsgi.url_scheme'] = 'http'

    # Call the target API
    result = request.get_raw_uri()
    print("get_raw_uri result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(HttpRequest.get_raw_uri))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()