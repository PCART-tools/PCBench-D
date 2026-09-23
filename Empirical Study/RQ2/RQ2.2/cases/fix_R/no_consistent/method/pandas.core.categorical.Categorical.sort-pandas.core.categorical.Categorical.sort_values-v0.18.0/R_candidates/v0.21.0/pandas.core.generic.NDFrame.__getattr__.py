    def __getattr__(self, name):
        """After regular attribute access, try looking up the name
        This allows simpler access to columns for interactive use.
        """

        # Note: obj.x will always call obj.__getattribute__('x') prior to
        # calling obj.__getattr__('x').

        if (name in self._internal_names_set or name in self._metadata or
                name in self._accessors):
            return object.__getattribute__(self, name)
        else:
            if name in self._info_axis:
                return self[name]
            return object.__getattribute__(self, name)
