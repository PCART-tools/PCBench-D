    @asyncio.coroutine
    def finish(self):
        """Finalize an application.

        Deprecated alias for .cleanup()
        """
        warnings.warn("Use .cleanup() instead", DeprecationWarning)
        yield from self.cleanup()
