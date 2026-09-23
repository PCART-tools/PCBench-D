    @Appender(_shared_docs['rename'] % dict(axes='axes keywords for this'
                                            ' object', klass='NDFrame'))
    def rename(self, *args, **kwargs):

        axes, kwargs = self._construct_axes_from_arguments(args, kwargs)
        copy = kwargs.pop('copy', True)
        inplace = kwargs.pop('inplace', False)

        if kwargs:
            raise TypeError('rename() got an unexpected keyword '
                            'argument "{0}"'.format(list(kwargs.keys())[0]))

        if com._count_not_none(*axes.values()) == 0:
            raise TypeError('must pass an index to rename')

        # renamer function if passed a dict
        def _get_rename_function(mapper):
            if isinstance(mapper, (dict, ABCSeries)):

                def f(x):
                    if x in mapper:
                        return mapper[x]
                    else:
                        return x
            else:
                f = mapper

            return f

        self._consolidate_inplace()
        result = self if inplace else self.copy(deep=copy)

        # start in the axis order to eliminate too many copies
        for axis in lrange(self._AXIS_LEN):
            v = axes.get(self._AXIS_NAMES[axis])
            if v is None:
                continue
            f = _get_rename_function(v)

            baxis = self._get_block_manager_axis(axis)
            result._data = result._data.rename_axis(f, axis=baxis, copy=copy)
            result._clear_item_cache()

        if inplace:
            self._update_inplace(result._data)
        else:
            return result.__finalize__(self)
