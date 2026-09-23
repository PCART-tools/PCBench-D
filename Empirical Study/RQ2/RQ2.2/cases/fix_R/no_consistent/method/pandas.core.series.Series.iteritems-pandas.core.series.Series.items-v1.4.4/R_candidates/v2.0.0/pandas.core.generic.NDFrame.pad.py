    @doc(klass=_shared_doc_kwargs["klass"])
    def pad(
        self: NDFrameT,
        *,
        axis: None | Axis = None,
        inplace: bool_t = False,
        limit: None | int = None,
        downcast: dict | None = None,
    ) -> NDFrameT | None:
        """
        Synonym for :meth:`DataFrame.fillna` with ``method='ffill'``.

        .. deprecated:: 2.0

            {klass}.pad is deprecated. Use {klass}.ffill instead.

        Returns
        -------
        {klass} or None
            Object with missing values filled or None if ``inplace=True``.
        """
        warnings.warn(
            "DataFrame.pad/Series.pad is deprecated. Use "
            "DataFrame.ffill/Series.ffill instead",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self.ffill(axis=axis, inplace=inplace, limit=limit, downcast=downcast)
