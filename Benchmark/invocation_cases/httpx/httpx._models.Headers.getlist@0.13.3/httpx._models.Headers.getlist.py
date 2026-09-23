import httpx
import inspect

def main():
    headers = httpx.Headers({'Set-Cookie': 'id=a3fWa; Expires=Wed, 21 Oct 2025 07:28:00 GMT;'})
    result = headers.getlist('Set-Cookie')
    print("getlist result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(httpx.Headers.getlist))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()