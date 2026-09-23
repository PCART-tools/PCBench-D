    def __dir__(self):
        """
        Provide method name lookup and completion
        Only provide 'public' methods.
        """
        rv = set(dir(type(self)))
        rv = (rv - self._dir_deletions()) | self._dir_additions()
        return sorted(rv)
