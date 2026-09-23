import redis
import inspect

def main():
    retry = redis.retry.Retry(backoff=None, retries=1)
    result = retry.update_supported_erros((Exception,))
    print("update_supported_errors result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(retry.update_supported_erros))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
