    def append(self, other: Series) -> Self:
        """
        Append a Series to this one.

        The resulting series will consist of multiple chunks.

        Parameters
        ----------
        other
            Series to append.

        Warnings
        --------
        This method modifies the series in-place. The series is returned for
        convenience only.

        See Also
        --------
        extend

        Examples
        --------
        >>> a = pl.Series("a", [1, 2, 3])
        >>> b = pl.Series("b", [4, 5])
        >>> a.append(b)
        shape: (5,)
        Series: 'a' [i64]
        [
            1
            2
            3
            4
            5
        ]

        The resulting series will consist of multiple chunks.

        >>> a.n_chunks()
        2

        """
        try:
            self._s.append(other._s)
        except RuntimeError as exc:
            if str(exc) == "Already mutably borrowed":
                self._s.append(other._s.clone())
            else:
                raise
        return self
