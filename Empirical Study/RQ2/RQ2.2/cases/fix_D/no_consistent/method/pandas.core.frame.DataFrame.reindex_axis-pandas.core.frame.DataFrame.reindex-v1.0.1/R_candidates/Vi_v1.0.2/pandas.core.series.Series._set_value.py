    def _set_value(self, label, value, takeable: bool = False):
        """
        Quickly set single value at passed label.

        If label is not contained, a new object is created with the label
        placed at the end of the result index.

        Parameters
        ----------
        label : object
            Partial indexing with MultiIndex not allowed.
        value : object
            Scalar value.
        takeable : interpret the index as indexers, default False

        Returns
        -------
        Series
            If label is contained, will be reference to calling Series,
            otherwise a new object.
        """
        try:
            if takeable:
                self._values[label] = value
            else:
                self.index._engine.set_value(self._values, label, value)
        except (KeyError, TypeError):
            # set using a non-recursive method
            self.loc[label] = value

        return self
