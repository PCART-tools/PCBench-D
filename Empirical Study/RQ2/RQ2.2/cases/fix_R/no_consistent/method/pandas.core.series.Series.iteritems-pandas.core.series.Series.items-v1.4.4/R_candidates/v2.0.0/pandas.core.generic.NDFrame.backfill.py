    @doc(klass=_shared_doc_kwargs["klass"])
    def backfill(
        self: NDFrameT,
        *,
        axis: None | Axis = None,
        inplace: bool_t = False,
        limit: None | int = None,
        downcast: dict | None = None,
    ) -> NDFrameT | None:
        """
        Synonym for :meth:`DataFrame.fillna` with ``method='bfill'``.

        .. deprecated:: 2.0

            {klass}.backfill is deprecated. Use {klass}.bfill instead.

        Returns
        -------
        {klass} or None
            Object with missing values filled or None if ``inplace=True``.
        """
        warnings.warn(
            "DataFrame.backfill/Series.backfill is deprecated. Use "
            "DataFrame.bfill/Series.bfill instead",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self.bfill(axis=axis, inplace=inplace, limit=limit, downcast=downcast)
