    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self"])
    def as_unordered(
        self, inplace: bool | NoDefault = no_default
    ) -> Categorical | None:
        """
        Set the Categorical to be unordered.

        Parameters
        ----------
        inplace : bool, default False
           Whether or not to set the ordered attribute in-place or return
           a copy of this categorical with ordered set to False.

           .. deprecated:: 1.5.0

        Returns
        -------
        Categorical or None
            Unordered Categorical or None if ``inplace=True``.
        """
        if inplace is not no_default:
            inplace = validate_bool_kwarg(inplace, "inplace")
        return self.set_ordered(False, inplace=inplace)
