    def is_regex_projection(self) -> bool:
        """
        Indicate if this expression expands to columns that match a regex pattern.

        Examples
        --------
        >>> e = pl.col("^.*$").alias("bar")
        >>> e.meta.is_regex_projection()
        True

        """
        return self._pyexpr.meta_is_regex_projection()
