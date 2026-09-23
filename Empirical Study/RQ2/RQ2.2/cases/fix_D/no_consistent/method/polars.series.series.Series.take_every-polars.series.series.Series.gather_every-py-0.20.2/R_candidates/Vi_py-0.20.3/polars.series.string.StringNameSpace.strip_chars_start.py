    def strip_chars_start(self, characters: IntoExprColumn | None = None) -> Series:
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
        >>> s = pl.Series([" hello ", "\tworld"])
        >>> s.str.strip_chars_start()
        shape: (2,)
        Series: '' [str]
        [
                "hello "
                "world"
        ]

        Characters can be stripped by passing a string as argument. Note that whitespace
        will not be stripped automatically when doing so.

        >>> s.str.strip_chars_start("wod\t")
        shape: (2,)
        Series: '' [str]
        [
                " hello "
                "rld"
        ]

        """
