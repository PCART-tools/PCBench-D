    def gt(self, other: Any) -> Self | Expr:
        """Method equivalent of operator expression `series > other`."""
        return self.__gt__(other)
