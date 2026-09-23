    def strip(self, characters: str | None = None) -> Expr:
        r"""
        Remove leading and trailing characters.

        Parameters
        ----------
        characters
            The set of characters to be removed. All combinations of this set of
            characters will be stripped. If set to None (default), all whitespace is
            removed instead.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [" hello", "\nworld"]})
        >>> df
        shape: (2, 1)
        ┌────────┐
        │ foo    │
        │ ---    │
        │ str    │
        ╞════════╡
        │  hello │
        │        │
        │ world  │
        └────────┘

        >>> df.select(pl.col("foo").str.strip())
        shape: (2, 1)
        ┌───────┐
        │ foo   │
        │ ---   │
        │ str   │
        ╞═══════╡
        │ hello │
        │ world │
        └───────┘

        Characters can be stripped by passing a string as argument. Note that whitespace
        will not be stripped automatically when doing so, unless that whitespace is
        also included in the string.

        >>> df.select(pl.col("foo").str.strip("ow\n"))
        shape: (2, 1)
        ┌───────┐
        │ foo   │
        │ ---   │
        │ str   │
        ╞═══════╡
        │  hell │
        │ rld   │
        └───────┘

        """
        return wrap_expr(self._pyexpr.str_strip(characters))
