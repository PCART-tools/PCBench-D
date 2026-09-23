    def join(self, other, how="left", level=None, return_indexers=False, sort=False):
        """
        See Index.join
        """
        self._assert_can_do_setop(other)

        if not isinstance(other, PeriodIndex):
            return self.astype(object).join(
                other, how=how, level=level, return_indexers=return_indexers, sort=sort
            )

        # _assert_can_do_setop ensures we have matching dtype
        result = super().join(
            other,
            how=how,
            level=level,
            return_indexers=return_indexers,
            sort=sort,
        )
        return result
