    def max(self, numeric_only=None, **kwargs):
        """
        The maximum value of the object.

        Only ordered `Categoricals` have a maximum!

        Raises
        ------
        TypeError
            If the `Categorical` is not `ordered`.

        Returns
        -------
        max : the maximum of this `Categorical`
        """
        self.check_for_ordered("max")
        if numeric_only:
            good = self._codes != -1
            pointer = self._codes[good].max(**kwargs)
        else:
            pointer = self._codes.max(**kwargs)
        if pointer == -1:
            return np.nan
        else:
            return self.categories[pointer]
