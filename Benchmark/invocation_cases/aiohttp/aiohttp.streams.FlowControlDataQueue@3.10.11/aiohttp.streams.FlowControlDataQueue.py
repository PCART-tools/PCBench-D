import aiohttp
import asyncio
import inspect

async def main():
    class CustomProtocol:
        _reading_paused = False

        def pause_reading(self):
            print("pause_reading called")
            self._reading_paused = True

        def resume_reading(self):
            print("resume_reading called")
            self._reading_paused = False

    loop = asyncio.get_event_loop()
    protocol = CustomProtocol()
    queue = aiohttp.FlowControlDataQueue(protocol, limit=1024, loop=loop)

    queue.feed_data(b"test data")
    result = await queue.read()
    print("FlowControlDataQueue read result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(aiohttp.FlowControlDataQueue))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    asyncio.run(main())
