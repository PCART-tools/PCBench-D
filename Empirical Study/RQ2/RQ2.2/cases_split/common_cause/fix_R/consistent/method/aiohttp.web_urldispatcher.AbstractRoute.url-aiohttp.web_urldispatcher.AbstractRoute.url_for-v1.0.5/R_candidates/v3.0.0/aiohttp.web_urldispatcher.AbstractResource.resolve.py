    @abc.abstractmethod  # pragma: no branch
    async def resolve(self, request):
        """Resolve resource

        Return (UrlMappingMatchInfo, allowed_methods) pair."""
