    def as_unordered(self, inplace=False):
        """
        Set the Categorical to be unordered.

        Parameters
        ----------
        inplace : bool, default False
           Whether or not to set the ordered attribute in-place or return
           a copy of this categorical with ordered set to False.

        Returns
        -------
        Categorical
            Unordered Categorical.
        """
        inplace = validate_bool_kwarg(inplace, "inplace")
        return self.set_ordered(False, inplace=inplace)
