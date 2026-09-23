    def set_value(self, label, value, takeable=False):
        """
        Quickly set single value at passed label.

        .. deprecated:: 0.21.0
            Please use .at[] or .iat[] accessors.

        If label is not contained, a new object is created with the label
        placed at the end of the result index.

        Parameters
        ----------
        label : object
            Partial indexing with MultiIndex not allowed
        value : object
            Scalar value
        takeable : interpret the index as indexers, default False

        Returns
        -------
        Series
            If label is contained, will be reference to calling Series,
            otherwise a new object.
        """
        warnings.warn(
            "set_value is deprecated and will be removed "
            "in a future release. Please use "
            ".at[] or .iat[] accessors instead",
            FutureWarning,
            stacklevel=2,
        )
        return self._set_value(label, value, takeable=takeable)
