import aiohttp
import asyncio
import inspect

async def main():
    reader = aiohttp.FlowControlStreamReader(None, limit=2**16)
    print("FlowControlStreamReader created:", reader)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(aiohttp.FlowControlStreamReader))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    asyncio.run(main())