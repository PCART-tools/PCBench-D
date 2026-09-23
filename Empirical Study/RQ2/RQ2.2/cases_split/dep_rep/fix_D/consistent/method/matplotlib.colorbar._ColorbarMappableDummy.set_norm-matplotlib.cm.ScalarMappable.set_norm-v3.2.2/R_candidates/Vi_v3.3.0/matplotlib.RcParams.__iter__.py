    def __iter__(self):
        """Yield sorted list of keys."""
        with cbook._suppress_matplotlib_deprecation_warning():
            yield from sorted(dict.__iter__(self))
