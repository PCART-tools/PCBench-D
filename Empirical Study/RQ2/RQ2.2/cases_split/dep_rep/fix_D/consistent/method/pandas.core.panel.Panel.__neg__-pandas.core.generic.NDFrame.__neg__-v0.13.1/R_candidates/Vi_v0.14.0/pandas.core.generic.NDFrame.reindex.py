    @Appender(_shared_docs['reindex'] % dict(axes="axes", klass="NDFrame"))
    def reindex(self, *args, **kwargs):

        # construct the args
        axes, kwargs = self._construct_axes_from_arguments(args, kwargs)
        method = com._clean_fill_method(kwargs.get('method'))
        level = kwargs.get('level')
        copy = kwargs.get('copy', True)
        limit = kwargs.get('limit')
        fill_value = kwargs.get('fill_value', np.nan)

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
        return self._reindex_axes(axes, level, limit,
                                  method, fill_value, copy).__finalize__(self)
