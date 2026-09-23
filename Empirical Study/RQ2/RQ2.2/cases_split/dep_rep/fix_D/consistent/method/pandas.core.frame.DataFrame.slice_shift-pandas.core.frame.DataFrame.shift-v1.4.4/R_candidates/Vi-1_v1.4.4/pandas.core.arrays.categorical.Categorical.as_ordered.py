    def as_ordered(self, inplace=False):
        """
        Set the Categorical to be ordered.

        Parameters
        ----------
        inplace : bool, default False
           Whether or not to set the ordered attribute in-place or return
           a copy of this categorical with ordered set to True.

        Returns
        -------
        Categorical or None
            Ordered Categorical or None if ``inplace=True``.
        """
        inplace = validate_bool_kwarg(inplace, "inplace")
        return self.set_ordered(True, inplace=inplace)
