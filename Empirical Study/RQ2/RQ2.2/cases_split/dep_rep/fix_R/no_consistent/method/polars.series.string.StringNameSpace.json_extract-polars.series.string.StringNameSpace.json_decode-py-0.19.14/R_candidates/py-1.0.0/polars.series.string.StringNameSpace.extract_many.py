    @unstable()
    def extract_many(
        self,
        patterns: Series | list[str],
        *,
        ascii_case_insensitive: bool = False,
        overlapping: bool = False,
    ) -> Series:
        """
        Use the aho-corasick algorithm to extract many matches.

        Parameters
        ----------
        patterns
            String patterns to search.
        ascii_case_insensitive
            Enable ASCII-aware case insensitive matching.
            When this option is enabled, searching will be performed without respect
            to case for ASCII letters (a-z and A-Z) only.
        overlapping
            Whether matches may overlap.

        Examples
        --------
        >>> s = pl.Series("values", ["discontent"])
        >>> patterns = ["winter", "disco", "onte", "discontent"]
        >>> s.str.extract_many(patterns, overlapping=True)
        shape: (1,)
        Series: 'values' [list[str]]
        [
            ["disco", "onte", "discontent"]
        ]

        """
