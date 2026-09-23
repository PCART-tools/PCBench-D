    def set_na_rep(self, na_rep: str) -> "Styler":
        """
        Set the missing data representation on a Styler.

        .. versionadded:: 1.0.0

        Parameters
        ----------
        na_rep : str

        Returns
        -------
        self : Styler
        """
        self.na_rep = na_rep
        return self
