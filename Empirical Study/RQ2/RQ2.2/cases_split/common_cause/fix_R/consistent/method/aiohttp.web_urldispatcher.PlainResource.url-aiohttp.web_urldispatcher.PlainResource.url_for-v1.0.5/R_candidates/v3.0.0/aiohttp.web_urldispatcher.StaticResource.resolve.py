    async def resolve(self, request):
        path = request.rel_url.raw_path
        method = request.method
        allowed_methods = set(self._routes)
        if not path.startswith(self._prefix):
            return None, set()

        if method not in allowed_methods:
            return None, allowed_methods

        match_dict = {'filename': URL.build(path=path[len(self._prefix)+1:],
                                            encoded=True).path}
        return (UrlMappingMatchInfo(match_dict, self._routes[method]),
                allowed_methods)
