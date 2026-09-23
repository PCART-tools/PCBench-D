    def set_axis(self, labels, axis: Axis = 0, inplace: bool_t = False):
        """
        Assign desired index to given axis.

        Indexes for%(extended_summary_sub)s row labels can be changed by assigning
        a list-like or Index.

        Parameters
        ----------
        labels : list-like, Index
            The values for the new index.

        axis : %(axes_single_arg)s, default 0
            The axis to update. The value 0 identifies the rows%(axis_description_sub)s.

        inplace : bool, default False
            Whether to return a new %(klass)s instance.

        Returns
        -------
        renamed : %(klass)s or None
            An object of type %(klass)s or None if ``inplace=True``.

        See Also
        --------
        %(klass)s.rename_axis : Alter the name of the index%(see_also_sub)s.
        """
        self._check_inplace_and_allows_duplicate_labels(inplace)
        return self._set_axis_nocheck(labels, axis, inplace)
