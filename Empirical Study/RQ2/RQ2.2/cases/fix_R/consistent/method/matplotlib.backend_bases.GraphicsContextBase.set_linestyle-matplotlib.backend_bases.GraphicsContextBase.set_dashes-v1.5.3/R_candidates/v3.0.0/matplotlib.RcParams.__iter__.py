    def __iter__(self):
        """Yield sorted list of keys."""
        yield from sorted(dict.__iter__(self))
