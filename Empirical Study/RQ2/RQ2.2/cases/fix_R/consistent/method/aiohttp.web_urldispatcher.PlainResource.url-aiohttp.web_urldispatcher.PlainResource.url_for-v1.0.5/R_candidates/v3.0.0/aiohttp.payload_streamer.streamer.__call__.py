    def __call__(self, *args, **kwargs):
        return _stream_wrapper(self.coro, args, kwargs)
