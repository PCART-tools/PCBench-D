    def strip_chars_start(self, characters: str | None = None) -> Expr:
        r"""
        Remove leading characters.

        Parameters
        ----------
        characters
            The set of characters to be removed. All combinations of this set of
            characters will be stripped. If set to None (default), all whitespace is
            removed instead.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [" hello ", "\tworld"]})
        >>> df.select(pl.col("foo").str.strip_chars_start())
        shape: (2, 1)
        ┌────────┐
        │ foo    │
        │ ---    │
        │ str    │
        ╞════════╡
        │ hello  │
        │ world  │
        └────────┘

        Characters can be stripped by passing a string as argument. Note that whitespace
        will not be stripped automatically when doing so.

        >>> df.select(pl.col("foo").str.strip_chars_start("wod\t"))
        shape: (2, 1)
        ┌─────────┐
        │ foo     │
        │ ---     │
        │ str     │
        ╞═════════╡
        │  hello  │
        │ rld     │
        └─────────┘

        """
        return wrap_expr(self._pyexpr.str_strip_chars_start(characters))
