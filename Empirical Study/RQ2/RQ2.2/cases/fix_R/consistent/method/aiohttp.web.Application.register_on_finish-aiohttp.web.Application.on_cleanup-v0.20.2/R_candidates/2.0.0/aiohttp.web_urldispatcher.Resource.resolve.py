    @asyncio.coroutine
    def resolve(self, request):
        allowed_methods = set()

        match_dict = self._match(request.rel_url.raw_path)
        if match_dict is None:
            return None, allowed_methods

        for route in self._routes:
            route_method = route.method
            allowed_methods.add(route_method)

            if (route_method == request._method or
                    route_method == hdrs.METH_ANY):
                return UrlMappingMatchInfo(match_dict, route), allowed_methods
        else:
            return None, allowed_methods

        yield  # pragma: no cover
