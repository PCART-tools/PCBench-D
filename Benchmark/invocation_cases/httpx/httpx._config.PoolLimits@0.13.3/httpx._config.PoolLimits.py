import httpx
import inspect

def main():
    pool_limits = httpx.PoolLimits(max_keepalive=10, max_connections=100)
    print("PoolLimits instance:", pool_limits)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(httpx.PoolLimits))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()