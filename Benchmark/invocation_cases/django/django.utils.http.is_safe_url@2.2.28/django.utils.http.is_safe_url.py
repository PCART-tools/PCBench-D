import inspect
from django.utils.http import is_safe_url
from urllib.parse import urlparse

def main():
    # Test data
    url = "http://example.com"
    allowed_hosts = ["example.com"]
    result = is_safe_url(url, allowed_hosts=allowed_hosts)
    print("is_safe_url result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(is_safe_url))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()