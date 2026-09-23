    def get_value(self, *args, **kwargs):
        """Quickly retrieve single value at (item, major, minor) location

        .. deprecated:: 0.21.0

        Please use .at[] or .iat[] accessors.

        Parameters
        ----------
        item : item label (panel item)
        major : major axis label (panel item row)
        minor : minor axis label (panel item column)
        takeable : interpret the passed labels as indexers, default False

        Returns
        -------
        value : scalar value
        """
        warnings.warn("get_value is deprecated and will be removed "
                      "in a future release. Please use "
                      ".at[] or .iat[] accessors instead", FutureWarning,
                      stacklevel=2)
        return self._get_value(*args, **kwargs)
