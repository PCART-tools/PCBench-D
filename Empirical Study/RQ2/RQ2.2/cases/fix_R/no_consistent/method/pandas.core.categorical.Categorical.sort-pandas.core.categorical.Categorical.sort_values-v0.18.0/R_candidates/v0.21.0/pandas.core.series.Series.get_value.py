    def get_value(self, label, takeable=False):
        """
        Quickly retrieve single value at passed index label

        .. deprecated:: 0.21.0

        Please use .at[] or .iat[] accessors.

        Parameters
        ----------
        index : label
        takeable : interpret the index as indexers, default False

        Returns
        -------
        value : scalar value
        """
        warnings.warn("get_value is deprecated and will be removed "
                      "in a future release. Please use "
                      ".at[] or .iat[] accessors instead", FutureWarning,
                      stacklevel=2)
        return self._get_value(label, takeable=takeable)
