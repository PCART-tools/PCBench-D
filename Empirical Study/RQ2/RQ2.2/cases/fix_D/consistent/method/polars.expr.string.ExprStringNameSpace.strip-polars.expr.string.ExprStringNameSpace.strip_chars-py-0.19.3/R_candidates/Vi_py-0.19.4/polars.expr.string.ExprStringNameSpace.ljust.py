    def ljust(self, width: int, fill_char: str = " ") -> Expr:
        """
        Return the string left justified in a string of length ``width``.

        Padding is done using the specified ``fill_char``.
        The original string is returned if ``width`` is less than or equal to
        ``len(s)``.

        Parameters
        ----------
        width
            Justify left to this length.
        fill_char
            Fill with this ASCII character.

        Examples
        --------
        >>> df = pl.DataFrame({"a": ["cow", "monkey", None, "hippopotamus"]})
        >>> df.select(pl.col("a").str.ljust(8, "*"))
        shape: (4, 1)
        ┌──────────────┐
        │ a            │
        │ ---          │
        │ str          │
        ╞══════════════╡
        │ cow*****     │
        │ monkey**     │
        │ null         │
        │ hippopotamus │
        └──────────────┘

        """
        return wrap_expr(self._pyexpr.str_ljust(width, fill_char))
