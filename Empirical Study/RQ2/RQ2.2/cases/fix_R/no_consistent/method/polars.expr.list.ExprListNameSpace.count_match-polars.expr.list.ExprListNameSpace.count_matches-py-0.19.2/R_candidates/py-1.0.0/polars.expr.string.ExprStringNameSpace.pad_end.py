    def pad_end(self, length: int, fill_char: str = " ") -> Expr:
        """
        Pad the end of the string until it reaches the given length.

        Parameters
        ----------
        length
            Pad the string until it reaches this length. Strings with length equal to
            or greater than this value are returned as-is.
        fill_char
            The character to pad the string with.

        See Also
        --------
        pad_start

        Examples
        --------
        >>> df = pl.DataFrame({"a": ["cow", "monkey", "hippopotamus", None]})
        >>> df.with_columns(padded=pl.col("a").str.pad_end(8, "*"))
        shape: (4, 2)
        ┌──────────────┬──────────────┐
        │ a            ┆ padded       │
        │ ---          ┆ ---          │
        │ str          ┆ str          │
        ╞══════════════╪══════════════╡
        │ cow          ┆ cow*****     │
        │ monkey       ┆ monkey**     │
        │ hippopotamus ┆ hippopotamus │
        │ null         ┆ null         │
        └──────────────┴──────────────┘
        """
        return wrap_expr(self._pyexpr.str_pad_end(length, fill_char))
