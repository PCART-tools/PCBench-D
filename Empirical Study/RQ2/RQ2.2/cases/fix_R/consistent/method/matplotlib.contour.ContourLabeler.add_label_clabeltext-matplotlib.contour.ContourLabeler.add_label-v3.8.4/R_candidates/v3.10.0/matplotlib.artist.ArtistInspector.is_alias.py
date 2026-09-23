    @staticmethod
    @cache
    def is_alias(method):
        """
        Return whether the object *method* is an alias for another method.
        """

        ds = inspect.getdoc(method)
        if ds is None:
            return False

        return ds.startswith('Alias for ')
