    def ffill(
        self: FrameOrSeries,
        axis=None,
        inplace: bool_t = False,
        limit=None,
        downcast=None,
    ) -> Optional[FrameOrSeries]:
        """
        Synonym for :meth:`DataFrame.fillna` with ``method='ffill'``.

        Returns
        -------
        %(klass)s or None
            Object with missing values filled or None if ``inplace=True``.
        """
        return self.fillna(
            method="ffill", axis=axis, inplace=inplace, limit=limit, downcast=downcast
        )
