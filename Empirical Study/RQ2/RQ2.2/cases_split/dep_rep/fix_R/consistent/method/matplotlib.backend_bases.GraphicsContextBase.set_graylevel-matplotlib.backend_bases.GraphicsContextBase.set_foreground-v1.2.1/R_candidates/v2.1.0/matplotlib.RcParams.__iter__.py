    def __iter__(self):
        """
        Yield sorted list of keys.
        """
        for k in sorted(dict.__iter__(self)):
            yield k
