    def join(
        self,
        other,
        how: str = "left",
        level=None,
        return_indexers: bool = False,
        sort: bool = False,
    ):
        """
        See Index.join
        """
        pself, pother = self._maybe_promote(other)
        if pself is not self or pother is not other:
            return pself.join(
                pother, how=how, level=level, return_indexers=return_indexers, sort=sort
            )

        self._maybe_utc_convert(other)  # raises if we dont have tzawareness compat
        return Index.join(
            self,
            other,
            how=how,
            level=level,
            return_indexers=return_indexers,
            sort=sort,
        )
