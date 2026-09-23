    def clear(self, n: int = 0) -> Series:
        """
        Create an empty copy of the current Series, with zero to 'n' elements.

        The copy has an identical name/dtype, but no data.

        Parameters
        ----------
        n
            Number of (empty) elements to return in the cleared frame.

        See Also
        --------
        clone : Cheap deepcopy/clone.

        Examples
        --------
        >>> s = pl.Series("a", [None, True, False])
        >>> s.clear()
        shape: (0,)
        Series: 'a' [bool]
        [
        ]

        >>> s.clear(n=2)
        shape: (2,)
        Series: 'a' [bool]
        [
            null
            null
        ]
        """
        if n < 0:
            msg = f"`n` should be greater than or equal to 0, got {n}"
            raise ValueError(msg)
        # faster path
        if n == 0:
            return self._from_pyseries(self._s.clear())
        s = (
            self.__class__(name=self.name, values=[], dtype=self.dtype)
            if len(self) > 0
            else self.clone()
        )
        return s.extend_constant(None, n=n) if n > 0 else s
