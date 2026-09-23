    async def cleanup(self):
        """Causes on_cleanup signal

        Should be called after shutdown()
        """
        await self.on_cleanup.send(self)
