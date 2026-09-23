    def _set_value(self, *args, **kwargs):
        # require an arg for each axis and the value
        nargs = len(args)
        nreq = self._AXIS_LEN + 1

        if nargs != nreq:
            raise TypeError('There must be an argument for each axis plus the '
                            'value provided, you gave {0} args, but {1} are '
                            'required'.format(nargs, nreq))
        takeable = kwargs.pop('takeable', None)

        if kwargs:
            raise TypeError('set_value() got an unexpected keyword '
                            'argument "{0}"'.format(list(kwargs.keys())[0]))

        try:
            if takeable is True:
                lower = self._iget_item_cache(args[0])
            else:
                lower = self._get_item_cache(args[0])

            lower._set_value(*args[1:], takeable=takeable)
            return self
        except KeyError:
            axes = self._expand_axes(args)
            d = self._construct_axes_dict_from(self, axes, copy=False)
            result = self.reindex(**d)
            args = list(args)
            likely_dtype, args[-1] = infer_dtype_from_scalar(args[-1])
            made_bigger = not np.array_equal(axes[0], self._info_axis)
            # how to make this logic simpler?
            if made_bigger:
                maybe_cast_item(result, args[0], likely_dtype)

            return result._set_value(*args)
