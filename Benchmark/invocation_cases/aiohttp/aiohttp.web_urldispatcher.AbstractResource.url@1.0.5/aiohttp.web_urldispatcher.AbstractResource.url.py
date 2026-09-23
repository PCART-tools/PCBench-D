import aiohttp
import inspect
from aiohttp import web
from aiohttp.web_urldispatcher import AbstractResource, UrlMappingMatchInfo

class HelloResource(AbstractResource):
    def __init__(self, path="/hello"):
        super().__init__()
        self._path = path
        self._routes = {}
        self._handler = None

    def set_handler(self, handler):
        self._handler = handler

    def __iter__(self):
        if self._handler:
            yield self._handler

    def __len__(self):
        return 1 if self._handler else 0

    def get_info(self):
        return {"path": self._path}

    async def resolve(self, request):
        if request.path != self._path:
            return None
        if self._handler is None:
            return None
        return UrlMappingMatchInfo({}, self._handler, self)
    
    def add_prefix(self, prefix: str) -> None:
        pass

    def url_for(self, **kwargs: str):
        return None

    def url(self, *, parts=None, query=None):
        super().url()
        return self._path


def main():
    app = web.Application()

    resource = HelloResource("/hello")
    url = resource.url()
    print("Resource URL:", url)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(AbstractResource.url))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()