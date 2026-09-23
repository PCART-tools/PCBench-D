    def __iter__(self):
        """
        so `dict(model)` works
        """
        yield from self._iter()
