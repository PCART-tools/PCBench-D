    def join(
        self, other, how: str = "left", level=None, return_indexers=False, sort=False
    ):
        """
        See Index.join
        """
        pself, pother = self._maybe_promote(other)
        if pself is not self or pother is not other:
            return pself.join(
                pother, how=how, level=level, return_indexers=return_indexers, sort=sort
            )

        this, other = self._maybe_utc_convert(other)
        return Index.join(
            this,
            other,
            how=how,
            level=level,
            return_indexers=return_indexers,
            sort=sort,
        )
