import aiohttp
import asyncio
from aiohttp.web_reqrep import StreamResponse
from email.utils import formatdate
import inspect

class DummyWriter: 
    def write_headers(self, status_line, headers):
        pass

    def write(self, data):
        pass

    @asyncio.coroutine 
    def drain(self):
        yield from asyncio.sleep(0)
    
    def set_tcp_nodelay(self,any):
        pass
    
    def set_tcp_cork(self,any):
        pass

class DummyTimeService:
    def strtime(self):
        return formatdate(usegmt=True)

class DummyRequest:
    keep_alive = True
    version = (1, 1)
    headers = {}

    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self._writer = DummyWriter()
        self._payload_writer = self._writer  
        self._task = None
        self._protocol = None
        self._message = type("DummyMessage", (), {"headers": {}})()
        self._transport = None
        self._read_bytes = 0
        self._client_max_size = 1024**2
        self._time_service = DummyTimeService()
        self.time_service = DummyTimeService()

@asyncio.coroutine
def main():
    req = DummyRequest()
    resp = StreamResponse()
    impl = resp.start(req)
    print("StreamResponse.start result:", impl)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(resp.start))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
