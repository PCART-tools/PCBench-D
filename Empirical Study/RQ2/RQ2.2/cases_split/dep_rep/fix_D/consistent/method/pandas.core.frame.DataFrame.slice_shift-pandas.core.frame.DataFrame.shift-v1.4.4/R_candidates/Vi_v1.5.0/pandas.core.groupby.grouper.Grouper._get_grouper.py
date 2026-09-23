    def _get_grouper(
        self, obj: NDFrameT, validate: bool = True
    ) -> tuple[Any, ops.BaseGrouper, NDFrameT]:
        """
        Parameters
        ----------
        obj : Series or DataFrame
        validate : bool, default True
            if True, validate the grouper

        Returns
        -------
        a tuple of binner, grouper, obj (possibly sorted)
        """
        self._set_grouper(obj)
        # error: Value of type variable "NDFrameT" of "get_grouper" cannot be
        # "Optional[Any]"
        # error: Incompatible types in assignment (expression has type "BaseGrouper",
        # variable has type "None")
        self.grouper, _, self.obj = get_grouper(  # type: ignore[type-var,assignment]
            self.obj,
            [self.key],
            axis=self.axis,
            level=self.level,
            sort=self.sort,
            validate=validate,
            dropna=self.dropna,
        )

        # error: Incompatible return value type (got "Tuple[None, None, None]",
        # expected "Tuple[Any, BaseGrouper, NDFrameT]")
        return self.binner, self.grouper, self.obj  # type: ignore[return-value]
