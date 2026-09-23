    def __getattr__(self, name):
        """After regular attribute access, try looking up the name of a the
        info.

        This allows simpler access to columns for interactive use.
        """
        if name in self._info_axis:
            return self[name]
        raise AttributeError("'%s' object has no attribute '%s'" %
                             (type(self).__name__, name))
