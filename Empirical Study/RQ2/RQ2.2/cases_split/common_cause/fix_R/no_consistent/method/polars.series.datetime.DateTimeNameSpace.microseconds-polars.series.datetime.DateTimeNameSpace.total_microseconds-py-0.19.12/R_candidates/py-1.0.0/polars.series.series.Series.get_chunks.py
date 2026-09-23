    def get_chunks(self) -> list[Series]:
        """
        Get the chunks of this Series as a list of Series.

        Examples
        --------
        >>> s1 = pl.Series("a", [1, 2, 3])
        >>> s2 = pl.Series("a", [4, 5, 6])
        >>> s = pl.concat([s1, s2], rechunk=False)
        >>> s.get_chunks()
        [shape: (3,)
        Series: 'a' [i64]
        [
                1
                2
                3
        ], shape: (3,)
        Series: 'a' [i64]
        [
                4
                5
                6
        ]]
        """
        return self._s.get_chunks()
