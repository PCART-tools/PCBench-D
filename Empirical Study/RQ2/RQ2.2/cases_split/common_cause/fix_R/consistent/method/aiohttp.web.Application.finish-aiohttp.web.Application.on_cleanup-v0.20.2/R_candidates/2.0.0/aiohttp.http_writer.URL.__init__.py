    def __init__(self, schema, netloc, port, path, query, fragment, userinfo):
        self._strict = False

        if port:
            netloc += ':{}'.format(port)
        if userinfo:
            netloc = yarl.quote(
                userinfo, safe='@:',
                protected=':', strict=False) + '@' + netloc

        if path:
            path = yarl.quote(path, safe='@:', protected='/', strict=False)

        if query:
            query = yarl.quote(
                query, safe='=+&?/:@',
                protected=yarl.PROTECT_CHARS, qs=True, strict=False)

        if fragment:
            fragment = yarl.quote(fragment, safe='?/:@', strict=False)

        self._val = SplitResult(
            schema or '',  # scheme
            netloc=netloc, path=path, query=query, fragment=fragment)
        self._cache = {}
