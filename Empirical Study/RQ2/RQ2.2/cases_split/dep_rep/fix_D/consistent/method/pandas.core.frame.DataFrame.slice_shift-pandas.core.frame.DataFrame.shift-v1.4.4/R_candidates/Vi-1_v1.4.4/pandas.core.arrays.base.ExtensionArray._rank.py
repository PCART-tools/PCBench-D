    def _rank(
        self,
        *,
        axis: int = 0,
        method: str = "average",
        na_option: str = "keep",
        ascending: bool = True,
        pct: bool = False,
    ):
        """
        See Series.rank.__doc__.
        """
        if axis != 0:
            raise NotImplementedError

        # TODO: we only have tests that get here with dt64 and td64
        # TODO: all tests that get here use the defaults for all the kwds
        return rank(
            self,
            axis=axis,
            method=method,
            na_option=na_option,
            ascending=ascending,
            pct=pct,
        )
