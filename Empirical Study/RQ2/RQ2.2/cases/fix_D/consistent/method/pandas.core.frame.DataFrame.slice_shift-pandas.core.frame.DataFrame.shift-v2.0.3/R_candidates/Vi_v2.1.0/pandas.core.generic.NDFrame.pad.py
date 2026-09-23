    @final
    @doc(klass=_shared_doc_kwargs["klass"])
    def pad(
        self,
        *,
        axis: None | Axis = None,
        inplace: bool_t = False,
        limit: None | int = None,
        downcast: dict | None | lib.NoDefault = lib.no_default,
    ) -> Self | None:
        """
        Fill NA/NaN values by propagating the last valid observation to next valid.

        .. deprecated:: 2.0

            {klass}.pad is deprecated. Use {klass}.ffill instead.

        Returns
        -------
        {klass} or None
            Object with missing values filled or None if ``inplace=True``.

        Examples
        --------
        Please see examples for :meth:`DataFrame.ffill` or :meth:`Series.ffill`.
        """
        warnings.warn(
            "DataFrame.pad/Series.pad is deprecated. Use "
            "DataFrame.ffill/Series.ffill instead",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self.ffill(axis=axis, inplace=inplace, limit=limit, downcast=downcast)
