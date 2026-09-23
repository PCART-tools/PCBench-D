    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # similar to _RequestContextManager, we do not need to check
        # for exceptions, response object can closes connection
        # is state is broken
        self.release()
