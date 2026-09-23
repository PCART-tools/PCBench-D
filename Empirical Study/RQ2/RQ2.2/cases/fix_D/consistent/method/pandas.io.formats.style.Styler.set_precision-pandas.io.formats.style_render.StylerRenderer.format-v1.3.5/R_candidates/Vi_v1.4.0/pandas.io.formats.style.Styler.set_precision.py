    def set_precision(self, precision: int) -> StylerRenderer:
        """
        Set the precision used to display values.

        .. deprecated:: 1.3.0

        Parameters
        ----------
        precision : int

        Returns
        -------
        self : Styler

        Notes
        -----
        This method is deprecated see `Styler.format`.
        """
        warnings.warn(
            "this method is deprecated in favour of `Styler.format(precision=..)`",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        self.precision = precision
        return self.format(precision=precision, na_rep=self.na_rep)
