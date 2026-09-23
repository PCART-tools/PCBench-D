    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self"])
    def as_ordered(self, inplace: bool | NoDefault = no_default) -> Categorical | None:
        """
        Set the Categorical to be ordered.

        Parameters
        ----------
        inplace : bool, default False
           Whether or not to set the ordered attribute in-place or return
           a copy of this categorical with ordered set to True.

           .. deprecated:: 1.5.0

        Returns
        -------
        Categorical or None
            Ordered Categorical or None if ``inplace=True``.
        """
        if inplace is not no_default:
            inplace = validate_bool_kwarg(inplace, "inplace")
        return self.set_ordered(True, inplace=inplace)
