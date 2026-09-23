    def _dir_additions(self):
        """
        Add additional __dir__ for this object.
        """
        rv = set()
        for accessor in self._accessors:
            try:
                getattr(self, accessor)
                rv.add(accessor)
            except AttributeError:
                pass
        return rv
