    def _shallow_copy(self, values=None, name: Label = no_default):
        """
        Create a new Index with the same class as the caller, don't copy the
        data, use the same object attributes with passed in attributes taking
        precedence.

        *this is an internal non-public method*

        Parameters
        ----------
        values : the values to create the new Index, optional
        name : Label, defaults to self.name
        """
        name = self.name if name is no_default else name

        if values is not None:
            return self._simple_new(values, name=name)

        result = self._simple_new(self._values, name=name)
        result._cache = self._cache
        return result
