    def set_value(self, label, value):
        """
        Quickly set single value at passed label. If label is not contained, a
        new object is created with the label placed at the end of the result
        index

        Parameters
        ----------
        label : object
            Partial indexing with MultiIndex not allowed
        value : object
            Scalar value

        Returns
        -------
        series : Series
            If label is contained, will be reference to calling Series,
            otherwise a new object
        """
        try:
            self.index._engine.set_value(self.values, label, value)
            return self
        except KeyError:

            # set using a non-recursive method
            self.loc[label] = value
            return self
