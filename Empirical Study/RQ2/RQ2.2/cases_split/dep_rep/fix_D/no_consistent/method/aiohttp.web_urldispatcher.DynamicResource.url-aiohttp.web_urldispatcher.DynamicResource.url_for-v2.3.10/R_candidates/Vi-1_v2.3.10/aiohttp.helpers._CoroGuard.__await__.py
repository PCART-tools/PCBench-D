        def __await__(self):
            self._awaited = True
            return super().__await__()
