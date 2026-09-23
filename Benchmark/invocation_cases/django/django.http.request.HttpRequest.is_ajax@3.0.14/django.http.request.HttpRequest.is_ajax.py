import django
from django.http import HttpRequest
import inspect
from django.conf import settings

def main():
    # Configure Django settings
    settings.configure(DEFAULT_CHARSET='utf-8')

    # Simulate a request with the necessary headers
    request = HttpRequest()
    request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
    
    # Call the target API
    result = request.is_ajax()
    print("is_ajax result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(HttpRequest.is_ajax))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()