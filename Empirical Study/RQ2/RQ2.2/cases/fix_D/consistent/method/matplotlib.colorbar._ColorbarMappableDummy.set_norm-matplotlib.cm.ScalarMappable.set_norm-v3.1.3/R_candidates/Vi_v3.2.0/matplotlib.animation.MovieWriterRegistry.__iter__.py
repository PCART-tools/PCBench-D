    def __iter__(self):
        """Iterate over names of available writer class."""
        for name in self._registered:
            if self.is_available(name):
                yield name
