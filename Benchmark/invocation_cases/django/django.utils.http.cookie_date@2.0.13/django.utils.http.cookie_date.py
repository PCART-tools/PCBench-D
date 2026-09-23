import inspect
from django.utils.http import cookie_date

def main():
    import time
    timestamp = time.time()
    result = cookie_date(timestamp)
    print("cookie_date result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(cookie_date))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()