    def strip_chars(self, characters: IntoExprColumn | None = None) -> Series:
        r"""
        Remove leading and trailing characters.

        Parameters
        ----------
        characters
            The set of characters to be removed. All combinations of this set of
            characters will be stripped from the start and end of the string. If set to
            None (default), all leading and trailing whitespace is removed instead.

        Examples
        --------
        >>> s = pl.Series([" hello ", "\tworld"])
        >>> s.str.strip_chars()
        shape: (2,)
        Series: '' [str]
        [
                "hello"
                "world"
        ]

        Characters can be stripped by passing a string as argument. Note that whitespace
        will not be stripped automatically when doing so, unless that whitespace is
        also included in the string.

        >>> s.str.strip_chars("o ")
        shape: (2,)
        Series: '' [str]
        [
            "hell"
            "	world"
        ]
        """
