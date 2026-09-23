import asyncio
import inspect
from aiohttp import web


class DummyRequest:
    def __init__(self):
        self._post = None
        self._post_files_cache = None
        self._body = b'key=value'
        self.method = 'POST'
        self._headers = {'CONTENT-TYPE': 'application/x-www-form-urlencoded'}
        self.charset = 'utf-8'

    @property
    def content_type(self):
        return self._headers['CONTENT-TYPE']

    @property
    def headers(self):
        return self._headers

    @asyncio.coroutine
    def read(self):
        return self._body

@asyncio.coroutine
def main():
    req = DummyRequest()
    result = yield from web.Request.POST(req)
    print("Request.POST result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(web.Request.POST))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
