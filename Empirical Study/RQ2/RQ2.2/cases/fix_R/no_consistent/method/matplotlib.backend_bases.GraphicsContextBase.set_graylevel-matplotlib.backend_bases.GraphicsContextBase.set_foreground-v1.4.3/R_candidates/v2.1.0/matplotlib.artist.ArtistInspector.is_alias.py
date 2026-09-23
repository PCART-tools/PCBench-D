    def is_alias(self, o):
        """
        Return *True* if method object *o* is an alias for another
        function.
        """
        ds = o.__doc__
        if ds is None:
            return False
        return ds.startswith('alias for ')
