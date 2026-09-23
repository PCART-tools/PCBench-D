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
