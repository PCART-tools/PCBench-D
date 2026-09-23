    @final
    @doc(klass=_shared_doc_kwargs["klass"])
    def backfill(
        self,
        *,
        axis: None | Axis = None,
        inplace: bool_t = False,
        limit: None | int = None,
        downcast: dict | None | lib.NoDefault = lib.no_default,
    ) -> Self | None:
        """
        Fill NA/NaN values by using the next valid observation to fill the gap.

        .. deprecated:: 2.0

            {klass}.backfill is deprecated. Use {klass}.bfill instead.

        Returns
        -------
        {klass} or None
            Object with missing values filled or None if ``inplace=True``.

        Examples
        --------
        Please see examples for :meth:`DataFrame.bfill` or :meth:`Series.bfill`.
        """
        warnings.warn(
            "DataFrame.backfill/Series.backfill is deprecated. Use "
            "DataFrame.bfill/Series.bfill instead",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self.bfill(axis=axis, inplace=inplace, limit=limit, downcast=downcast)
