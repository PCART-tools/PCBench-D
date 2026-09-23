    def set_value(self, *args, **kwargs):
        """Quickly set single value at (item, major, minor) location

        .. deprecated:: 0.21.0

        Please use .at[] or .iat[] accessors.

        Parameters
        ----------
        item : item label (panel item)
        major : major axis label (panel item row)
        minor : minor axis label (panel item column)
        value : scalar
        takeable : interpret the passed labels as indexers, default False

        Returns
        -------
        panel : Panel
            If label combo is contained, will be reference to calling Panel,
            otherwise a new object
        """
        warnings.warn("set_value is deprecated and will be removed "
                      "in a future release. Please use "
                      ".at[] or .iat[] accessors instead", FutureWarning,
                      stacklevel=2)
        return self._set_value(*args, **kwargs)
