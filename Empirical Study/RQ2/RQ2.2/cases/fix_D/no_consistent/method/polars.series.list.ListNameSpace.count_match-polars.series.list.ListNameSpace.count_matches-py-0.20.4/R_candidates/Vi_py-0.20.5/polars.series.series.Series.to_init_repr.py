    def to_init_repr(self, n: int = 1000) -> str:
        """
        Convert Series to instantiatable string representation.

        Parameters
        ----------
        n
            Only use first n elements.

        See Also
        --------
        polars.Series.to_init_repr
        polars.from_repr

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, None, 4], dtype=pl.Int16)
        >>> print(s.to_init_repr())
        pl.Series("a", [1, 2, None, 4], dtype=pl.Int16)
        >>> s_from_str_repr = eval(s.to_init_repr())
        >>> s_from_str_repr
        shape: (4,)
        Series: 'a' [i16]
        [
            1
            2
            null
            4
        ]
        """
        return (
            f'pl.Series("{self.name}", {self.head(n).to_list()}, dtype=pl.{self.dtype})'
        )
