import aiohttp
import asyncio
import inspect
from aiohttp.http_writer import PayloadWriter

class DummyStream:
    def __init__(self):
        self.available = True
        self.transport = None
        self._drain_called = False

    def acquire(self, writer):
        self.transport = writer._transport
        self.available = False

    def release(self):
        self.available = True

    def drain(self):
        self._drain_called = True
        return asyncio.sleep(0)

    @property
    def tcp_nodelay(self):
        return False

    def set_tcp_nodelay(self, value):
        pass

    @property
    def tcp_cork(self):
        return False

    def set_tcp_cork(self, value):
        pass

class DummyTransport:
    def __init__(self):
        self.buffer = []

    def write(self, data):
        self.buffer.append(data)

    def close(self):
        pass

    def is_closing(self):
        return False

async def main():
    loop = asyncio.get_event_loop()
    stream = DummyStream()
    stream.transport = DummyTransport()
    
    payload_writer = PayloadWriter(stream, loop)
    print("PayloadWriter instance created:", payload_writer)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(PayloadWriter))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    asyncio.run(main())
