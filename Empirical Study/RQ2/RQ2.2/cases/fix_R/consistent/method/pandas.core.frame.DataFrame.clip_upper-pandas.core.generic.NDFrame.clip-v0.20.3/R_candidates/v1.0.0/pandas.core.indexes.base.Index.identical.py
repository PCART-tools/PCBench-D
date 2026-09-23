    def identical(self, other) -> bool:
        """
        Similar to equals, but check that other comparable attributes are
        also equal.

        Returns
        -------
        bool
            If two Index objects have equal elements and same type True,
            otherwise False.
        """
        return (
            self.equals(other)
            and all(
                (
                    getattr(self, c, None) == getattr(other, c, None)
                    for c in self._comparables
                )
            )
            and type(self) == type(other)
        )
