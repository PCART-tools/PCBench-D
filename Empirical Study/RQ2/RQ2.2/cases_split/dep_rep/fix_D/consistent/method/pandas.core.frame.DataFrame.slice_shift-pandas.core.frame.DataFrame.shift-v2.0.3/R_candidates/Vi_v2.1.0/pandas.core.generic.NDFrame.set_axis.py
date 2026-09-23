    def set_axis(
        self,
        labels,
        *,
        axis: Axis = 0,
        copy: bool_t | None = None,
    ) -> Self:
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

        copy : bool, default True
            Whether to make a copy of the underlying data.

            .. versionadded:: 1.5.0

        Returns
        -------
        %(klass)s
            An object of type %(klass)s.

        See Also
        --------
        %(klass)s.rename_axis : Alter the name of the index%(see_also_sub)s.
        """
        return self._set_axis_nocheck(labels, axis, inplace=False, copy=copy)
