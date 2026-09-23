    @asyncio.coroutine
    @abc.abstractmethod  # pragma: no branch
    def resolve(self, request):
        """Resolve resource

        Return (UrlMappingMatchInfo, allowed_methods) pair."""
