    def is_alias(self, o):
        """Return whether method object *o* is an alias for another method."""
        ds = inspect.getdoc(o)
        if ds is None:
            return False
        return ds.startswith('Alias for ')
