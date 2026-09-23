    def sum_horizontal(self, *, ignore_nulls: bool = True) -> Series:
        """
        Sum all values horizontally across columns.

        Parameters
        ----------
        ignore_nulls
            Ignore null values (default).
            If set to `False`, any null value in the input will lead to a null output.

        Returns
        -------
        Series
            A Series named `"sum"`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [4.0, 5.0, 6.0],
        ...     }
        ... )
        >>> df.sum_horizontal()
        shape: (3,)
        Series: 'sum' [f64]
        [
                5.0
                7.0
                9.0
        ]
        """
        return wrap_s(self._df.sum_horizontal(ignore_nulls)).alias("sum")
