    def _agg_by_level(self, name, axis=0, level=0, skipna=True, **kwargs):
        if axis is None:
            raise ValueError("Must specify 'axis' when aggregating by level.")
        grouped = self.groupby(level=level, axis=axis, sort=False)
        if hasattr(grouped, name) and skipna:
            return getattr(grouped, name)(**kwargs)
        axis = self._get_axis_number(axis)
        method = getattr(type(self), name)
        applyf = lambda x: method(x, axis=axis, skipna=skipna, **kwargs)
        return grouped.aggregate(applyf)
