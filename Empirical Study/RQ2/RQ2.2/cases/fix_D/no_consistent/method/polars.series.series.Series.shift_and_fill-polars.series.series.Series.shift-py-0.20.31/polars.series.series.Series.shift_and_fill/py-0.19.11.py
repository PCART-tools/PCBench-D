    @deprecate_renamed_parameter("periods", "n", version="0.19.11")
    def shift_and_fill(
        self,
        fill_value: int | Expr,
        *,
        n: int = 1,
    ) -> Series:
        """
        Shift values by the given number of places and fill the resulting null values.

        Parameters
        ----------
        fill_value
            Fill None values with the result of this expression.
        n
            Number of places to shift (may be negative).

        """
