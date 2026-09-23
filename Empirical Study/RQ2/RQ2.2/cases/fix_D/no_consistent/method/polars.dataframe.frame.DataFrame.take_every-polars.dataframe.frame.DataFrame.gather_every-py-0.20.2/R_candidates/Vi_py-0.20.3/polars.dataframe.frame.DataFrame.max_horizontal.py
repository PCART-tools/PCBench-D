    def max_horizontal(self) -> Series:
        """
        Get the maximum value horizontally across columns.

        Returns
        -------
        Series
            A Series named `"max"`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [4.0, 5.0, 6.0],
        ...     }
        ... )
        >>> df.max_horizontal()
        shape: (3,)
        Series: 'max' [f64]
        [
                4.0
                5.0
                6.0
        ]
        """
        return self.select(max=F.max_horizontal(F.all())).to_series()
