class Timer:
    async def _get_time(self) -> float:
        library = sniffio.current_async_library()
        if library == "trio":
            import trio

            return trio.current_time()
        elif library == "curio":  # pragma: nocover
            import curio

            return await curio.clock()

        import asyncio

        return asyncio.get_event_loop().time()

    def sync_start(self) -> None:
        self.started = time.perf_counter()

    async def async_start(self) -> None:
        self.started = await self._get_time()

    def sync_elapsed(self) -> float:
        now = time.perf_counter()
        return now - self.started

    async def async_elapsed(self) -> float:
        now = await self._get_time()
        return now - self.started
