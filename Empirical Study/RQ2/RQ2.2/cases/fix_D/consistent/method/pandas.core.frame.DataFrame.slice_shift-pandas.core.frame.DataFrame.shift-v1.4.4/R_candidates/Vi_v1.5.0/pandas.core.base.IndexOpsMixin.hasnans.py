    @cache_readonly
    def hasnans(self) -> bool:
        """
        Return True if there are any NaNs.

        Enables various performance speedups.
        """
        # error: Item "bool" of "Union[bool, ndarray[Any, dtype[bool_]], NDFrame]"
        # has no attribute "any"
        return bool(isna(self).any())  # type: ignore[union-attr]
