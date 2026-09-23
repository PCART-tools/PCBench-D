    @Appender(_shared_docs['reindex'] % dict(axes="axes", klass="NDFrame",
                                             optional_labels="",
                                             optional_axis=""))
    def reindex(self, *args, **kwargs):

        # construct the args
        axes, kwargs = self._construct_axes_from_arguments(args, kwargs)
        method = missing.clean_reindex_fill_method(kwargs.pop('method', None))
        level = kwargs.pop('level', None)
        copy = kwargs.pop('copy', True)
        limit = kwargs.pop('limit', None)
        tolerance = kwargs.pop('tolerance', None)
        fill_value = kwargs.pop('fill_value', np.nan)

        # Series.reindex doesn't use / need the axis kwarg
        # We pop and ignore it here, to make writing Series/Frame generic code
        # easier
        kwargs.pop("axis", None)

        if kwargs:
            raise TypeError('reindex() got an unexpected keyword '
                            'argument "{0}"'.format(list(kwargs.keys())[0]))

        self._consolidate_inplace()

        # if all axes that are requested to reindex are equal, then only copy
        # if indicated must have index names equal here as well as values
        if all([self._get_axis(axis).identical(ax)
                for axis, ax in axes.items() if ax is not None]):
            if copy:
                return self.copy()
            return self

        # check if we are a multi reindex
        if self._needs_reindex_multi(axes, method, level):
            try:
                return self._reindex_multi(axes, copy, fill_value)
            except:
                pass

        # perform the reindex on the axes
        return self._reindex_axes(axes, level, limit, tolerance, method,
                                  fill_value, copy).__finalize__(self)
