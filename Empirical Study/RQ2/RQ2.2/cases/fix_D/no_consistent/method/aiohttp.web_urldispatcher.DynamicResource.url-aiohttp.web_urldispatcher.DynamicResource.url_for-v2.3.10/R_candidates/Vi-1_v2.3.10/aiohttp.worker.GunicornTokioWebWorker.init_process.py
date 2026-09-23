    def init_process(self):
        import tokio

        # Close any existing event loop before setting a
        # new policy.
        asyncio.get_event_loop().close()

        # Setup tokio policy, so that every
        # asyncio.get_event_loop() will create an instance
        # of tokio event loop.
        asyncio.set_event_loop_policy(tokio.EventLoopPolicy())

        super().init_process()
