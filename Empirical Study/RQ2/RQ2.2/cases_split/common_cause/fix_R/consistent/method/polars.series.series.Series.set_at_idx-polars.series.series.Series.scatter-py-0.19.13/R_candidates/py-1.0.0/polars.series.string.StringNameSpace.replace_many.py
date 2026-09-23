    def replace_many(
        self,
        patterns: Series | list[str],
        replace_with: Series | list[str] | str,
        *,
        ascii_case_insensitive: bool = False,
    ) -> Series:
        """
        Use the aho-corasick algorithm to replace many matches.

        Parameters
        ----------
        patterns
            String patterns to search and replace.
        replace_with
            Strings to replace where a pattern was a match.
            This can be broadcasted. So it supports many:one and many:many.
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
        >>> s.str.replace_many(["you", "me"], ["me", "you"])
        shape: (3,)
        Series: 'lyrics' [str]
        [
            "Everybody wants to rule the world"
            "Tell you what me want, what me really really want"
            "Can me feel the love tonight"
        ]
        """
