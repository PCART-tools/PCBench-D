    def external_values(self, dtype=None):
        """
        The array that Series.values returns (public attribute).

        This has some historical constraints, and is overridden in block
        subclasses to return the correct array (e.g. period returns
        object ndarray and datetimetz a datetime64[ns] ndarray instead of
        proper extension array).
        """
        return self.values
