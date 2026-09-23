    @final
    def identical(self, other) -> bool:
        """
        Similar to equals, but checks that object attributes and types are also equal.

        Returns
        -------
        bool
            If two Index objects have equal elements and same type True,
            otherwise False.

        Examples
        --------
        >>> idx1 = pd.Index(['1', '2', '3'])
        >>> idx2 = pd.Index(['1', '2', '3'])
        >>> idx2.identical(idx1)
        True

        >>> idx1 = pd.Index(['1', '2', '3'], name="A")
        >>> idx2 = pd.Index(['1', '2', '3'], name="B")
        >>> idx2.identical(idx1)
        False
        """
        return (
            self.equals(other)
            and all(
                getattr(self, c, None) == getattr(other, c, None)
                for c in self._comparables
            )
            and type(self) == type(other)
            and self.dtype == other.dtype
        )
