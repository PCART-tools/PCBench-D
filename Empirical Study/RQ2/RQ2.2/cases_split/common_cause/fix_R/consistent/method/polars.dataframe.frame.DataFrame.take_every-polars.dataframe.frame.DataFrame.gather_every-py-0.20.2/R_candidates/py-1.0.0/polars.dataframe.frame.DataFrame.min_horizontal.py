    def min_horizontal(self) -> Series:
        """
        Get the minimum value horizontally across columns.

        Returns
        -------
        Series
            A Series named `"min"`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [4.0, 5.0, 6.0],
        ...     }
        ... )
        >>> df.min_horizontal()
        shape: (3,)
        Series: 'min' [f64]
        [
                1.0
                2.0
                3.0
        ]
        """
        return self.select(min=F.min_horizontal(F.all())).to_series()
