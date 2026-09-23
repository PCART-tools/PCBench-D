    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self", "labels"])
    def set_axis(
        self: NDFrameT,
        labels,
        axis: Axis = 0,
        inplace: bool_t | lib.NoDefault = lib.no_default,
        *,
        copy: bool_t | lib.NoDefault = lib.no_default,
    ) -> NDFrameT | None:
        """
        Assign desired index to given axis.

        Indexes for%(extended_summary_sub)s row labels can be changed by assigning
        a list-like or Index.

        Parameters
        ----------
        labels : list-like, Index
            The values for the new index.

        axis : %(axes_single_arg)s, default 0
            The axis to update. The value 0 identifies the rows. For `Series`
            this parameter is unused and defaults to 0.

        inplace : bool, default False
            Whether to return a new %(klass)s instance.

            .. deprecated:: 1.5.0

        copy : bool, default True
            Whether to make a copy of the underlying data.

            .. versionadded:: 1.5.0

        Returns
        -------
        renamed : %(klass)s or None
            An object of type %(klass)s or None if ``inplace=True``.

        See Also
        --------
        %(klass)s.rename_axis : Alter the name of the index%(see_also_sub)s.
        """
        if inplace is not lib.no_default:
            warnings.warn(
                f"{type(self).__name__}.set_axis 'inplace' keyword is deprecated "
                "and will be removed in a future version. Use "
                "`obj = obj.set_axis(..., copy=False)` instead",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
        else:
            inplace = False

        if inplace:
            if copy is True:
                raise ValueError("Cannot specify both inplace=True and copy=True")
            copy = False
        elif copy is lib.no_default:
            copy = True

        self._check_inplace_and_allows_duplicate_labels(inplace)
        return self._set_axis_nocheck(labels, axis, inplace, copy=copy)
