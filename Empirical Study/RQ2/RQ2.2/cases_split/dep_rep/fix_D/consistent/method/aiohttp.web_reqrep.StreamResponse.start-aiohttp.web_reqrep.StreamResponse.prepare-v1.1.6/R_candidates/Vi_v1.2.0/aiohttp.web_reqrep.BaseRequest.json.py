    @asyncio.coroutine
    def json(self, *, loads=json.loads, loader=None):
        """Return BODY as JSON."""
        if loader is not None:
            warnings.warn(
                "Using loader argument is deprecated, use loads instead",
                DeprecationWarning)
            loads = loader
        body = yield from self.text()
        return loads(body)
