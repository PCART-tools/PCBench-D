    def __call__(self):
        return RequestHandler(self, loop=self._loop, **self._kwargs)
