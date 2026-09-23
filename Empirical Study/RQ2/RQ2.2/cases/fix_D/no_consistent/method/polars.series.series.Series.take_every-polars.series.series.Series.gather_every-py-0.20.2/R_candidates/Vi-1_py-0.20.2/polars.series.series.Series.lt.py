    def lt(self, other: Any) -> Self | Expr:
        """Method equivalent of operator expression `series < other`."""
        return self.__lt__(other)
