    def mean_horizontal(self, *, ignore_nulls: bool = True) -> Series:
        """
        Take the mean of all values horizontally across columns.

        Parameters
        ----------
        ignore_nulls
            Ignore null values (default).
            If set to `False`, any null value in the input will lead to a null output.

        Returns
        -------
        Series
            A Series named `"mean"`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [4.0, 5.0, 6.0],
        ...     }
        ... )
        >>> df.mean_horizontal()
        shape: (3,)
        Series: 'mean' [f64]
        [
                2.5
                3.5
                4.5
        ]
        """
        return wrap_s(self._df.mean_horizontal(ignore_nulls)).alias("mean")
