    def set_value(self, label, value, takeable=False):
        """
        Quickly set single value at passed label. If label is not contained, a
        new object is created with the label placed at the end of the result
        index

        .. deprecated:: 0.21.0

        Please use .at[] or .iat[] accessors.

        Parameters
        ----------
        label : object
            Partial indexing with MultiIndex not allowed
        value : object
            Scalar value
        takeable : interpret the index as indexers, default False

        Notes
        -----
        This method *always* returns a new object. It is not particularly
        efficient but is provided for API compatibility with Series

        Returns
        -------
        series : SparseSeries
        """
        warnings.warn(
            "set_value is deprecated and will be removed "
            "in a future release. Please use "
            ".at[] or .iat[] accessors instead",
            FutureWarning,
            stacklevel=2,
        )
        return self._set_value(label, value, takeable=takeable)
