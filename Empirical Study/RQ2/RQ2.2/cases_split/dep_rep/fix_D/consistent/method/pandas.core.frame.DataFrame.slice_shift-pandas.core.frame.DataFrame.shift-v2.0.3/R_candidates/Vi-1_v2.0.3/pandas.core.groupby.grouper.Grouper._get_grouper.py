    def _get_grouper(
        self, obj: NDFrameT, validate: bool = True
    ) -> tuple[ops.BaseGrouper, NDFrameT]:
        """
        Parameters
        ----------
        obj : Series or DataFrame
        validate : bool, default True
            if True, validate the grouper

        Returns
        -------
        a tuple of grouper, obj (possibly sorted)
        """
        obj, _, _ = self._set_grouper(obj)
        grouper, _, obj = get_grouper(
            obj,
            [self.key],
            axis=self.axis,
            level=self.level,
            sort=self.sort,
            validate=validate,
            dropna=self.dropna,
        )
        # Without setting this, subsequent lookups to .groups raise
        # error: Incompatible types in assignment (expression has type "BaseGrouper",
        # variable has type "None")
        self._grouper_deprecated = grouper  # type: ignore[assignment]

        return grouper, obj
