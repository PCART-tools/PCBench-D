import requests
from requests.adapters import HTTPAdapter
import inspect

def main():
    adapter = HTTPAdapter()

    req = requests.Request(
        method="GET",
        url="http://example.com"
    ).prepare()
    verify = True
    conn = adapter._get_connection(
        request=req,
        verify=verify,
        proxies=None,
        cert=None
    )

    print("connection:", conn)
    
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(HTTPAdapter._get_connection))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()