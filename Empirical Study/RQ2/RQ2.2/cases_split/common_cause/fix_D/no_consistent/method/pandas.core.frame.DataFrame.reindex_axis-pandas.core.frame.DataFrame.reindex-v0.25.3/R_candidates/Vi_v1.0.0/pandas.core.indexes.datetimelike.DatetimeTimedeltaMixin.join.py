    def join(
        self, other, how: str = "left", level=None, return_indexers=False, sort=False
    ):
        """
        See Index.join
        """
        if self._is_convertible_to_index_for_join(other):
            try:
                other = type(self)(other)
            except (TypeError, ValueError):
                pass

        this, other = self._maybe_utc_convert(other)
        return Index.join(
            this,
            other,
            how=how,
            level=level,
            return_indexers=return_indexers,
            sort=sort,
        )
