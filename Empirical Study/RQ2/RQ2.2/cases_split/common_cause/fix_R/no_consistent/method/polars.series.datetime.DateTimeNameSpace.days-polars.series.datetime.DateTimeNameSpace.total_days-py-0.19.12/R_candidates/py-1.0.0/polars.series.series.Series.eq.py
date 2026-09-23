    def eq(self, other: Any) -> Series | Expr:
        """Method equivalent of operator expression `series == other`."""
        return self.__eq__(other)
