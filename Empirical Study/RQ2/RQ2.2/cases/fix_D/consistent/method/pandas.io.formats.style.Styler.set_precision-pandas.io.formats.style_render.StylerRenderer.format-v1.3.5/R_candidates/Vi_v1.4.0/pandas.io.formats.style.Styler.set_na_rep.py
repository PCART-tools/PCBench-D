    def set_na_rep(self, na_rep: str) -> StylerRenderer:
        """
        Set the missing data representation on a ``Styler``.

        .. versionadded:: 1.0.0

        .. deprecated:: 1.3.0

        Parameters
        ----------
        na_rep : str

        Returns
        -------
        self : Styler

        Notes
        -----
        This method is deprecated. See `Styler.format()`
        """
        warnings.warn(
            "this method is deprecated in favour of `Styler.format(na_rep=..)`",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        self.na_rep = na_rep
        return self.format(na_rep=na_rep, precision=self.precision)
