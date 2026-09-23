    def contains_any(
        self, patterns: Series | list[str], *, ascii_case_insensitive: bool = False
    ) -> Series:
        """
        Use the aho-corasick algorithm to find matches.

        This version determines if any of the patterns find a match.

        Parameters
        ----------
        patterns
            String patterns to search.
        ascii_case_insensitive
            Enable ASCII-aware case insensitive matching.
            When this option is enabled, searching will be performed without respect
            to case for ASCII letters (a-z and A-Z) only.

        Examples
        --------
        >>> _ = pl.Config.set_fmt_str_lengths(100)
        >>> s = pl.Series(
        ...     "lyrics",
        ...     [
        ...         "Everybody wants to rule the world",
        ...         "Tell me what you want, what you really really want",
        ...         "Can you feel the love tonight",
        ...     ],
        ... )
        >>> s.str.contains_any(["you", "me"])
        shape: (3,)
        Series: 'lyrics' [bool]
        [
            false
            true
            true
        ]
        """
