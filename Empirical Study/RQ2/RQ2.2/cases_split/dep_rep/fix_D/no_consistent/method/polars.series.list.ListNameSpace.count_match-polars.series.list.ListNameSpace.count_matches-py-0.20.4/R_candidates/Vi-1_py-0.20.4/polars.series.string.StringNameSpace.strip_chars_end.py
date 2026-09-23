    def strip_chars_end(self, characters: IntoExprColumn | None = None) -> Series:
        r"""
        Remove trailing characters.

        Parameters
        ----------
        characters
            The set of characters to be removed. All combinations of this set of
            characters will be stripped. If set to None (default), all whitespace is
            removed instead.

        Examples
        --------
        >>> s = pl.Series([" hello ", "world\t"])
        >>> s.str.strip_chars_end()
        shape: (2,)
        Series: '' [str]
        [
                " hello"
                "world"
        ]

        Characters can be stripped by passing a string as argument. Note that whitespace
        will not be stripped automatically when doing so.

        >>> s.str.strip_chars_end("orld\t")
        shape: (2,)
        Series: '' [str]
        [
            " hello "
            "w"
        ]
        """
