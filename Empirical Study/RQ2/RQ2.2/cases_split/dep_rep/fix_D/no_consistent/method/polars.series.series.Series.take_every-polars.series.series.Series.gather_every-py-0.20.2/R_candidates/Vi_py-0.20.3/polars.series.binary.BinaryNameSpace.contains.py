    def contains(self, literal: IntoExpr) -> Series:
        """
        Check if binaries in Series contain a binary substring.

        Parameters
        ----------
        literal
            The binary substring to look for

        Returns
        -------
        Series
            Series of data type :class:`Boolean`.

        """
