    def mad(
        self,
        axis: Axis | None = None,
        skipna: bool_t = True,
        level: Level | None = None,
    ) -> Series | float:
        """
        {desc}

        Parameters
        ----------
        axis : {axis_descr}
            Axis for the function to be applied on.
        skipna : bool, default True
            Exclude NA/null values when computing the result.
        level : int or level name, default None
            If the axis is a MultiIndex (hierarchical), count along a
            particular level, collapsing into a {name1}.

        Returns
        -------
        {name1} or {name2} (if level specified)\
        {see_also}\
        {examples}
        """
        if not is_bool(skipna):
            warnings.warn(
                "Passing None for skipna is deprecated and will raise in a future"
                "version. Pass True instead. Only boolean values will be allowed "
                "in the future.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            skipna = True
        if axis is None:
            axis = self._stat_axis_number
        if level is not None:
            warnings.warn(
                "Using the level keyword in DataFrame and Series aggregations is "
                "deprecated and will be removed in a future version. Use groupby "
                "instead. df.mad(level=1) should use df.groupby(level=1).mad()",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            return self._agg_by_level("mad", axis=axis, level=level, skipna=skipna)

        data = self._get_numeric_data()
        if axis == 0:
            demeaned = data - data.mean(axis=0)
        else:
            demeaned = data.sub(data.mean(axis=1), axis=0)
        return np.abs(demeaned).mean(axis=axis, skipna=skipna)
