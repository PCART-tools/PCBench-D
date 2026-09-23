    @abstractmethod  # pragma: no cover
    @asyncio.coroutine
    def _make_factory(self, **kwargs):
        pass
