    async def cleanup(self):
        loop = asyncio.get_event_loop()

        if self._server is None:
            # no started yet, do nothing
            return

        # The loop over sites is intentional, an exception on gather()
        # leaves self._sites in unpredictable state.
        # The loop guaranties that a site is either deleted on success or
        # still present on failure
        for site in list(self._sites):
            await site.stop()
        await self._cleanup_server()
        self._server = None
        if self._handle_signals:
            try:
                loop.remove_signal_handler(signal.SIGINT)
                loop.remove_signal_handler(signal.SIGTERM)
            except NotImplementedError:  # pragma: no cover
                # remove_signal_handler is not implemented on Windows
                pass
