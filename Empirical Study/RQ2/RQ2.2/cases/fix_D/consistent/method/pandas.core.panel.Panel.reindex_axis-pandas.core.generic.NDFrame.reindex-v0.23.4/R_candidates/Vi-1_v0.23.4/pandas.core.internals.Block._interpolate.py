    def _interpolate(self, method=None, index=None, values=None,
                     fill_value=None, axis=0, limit=None,
                     limit_direction='forward', limit_area=None,
                     inplace=False, downcast=None, mgr=None, **kwargs):
        """ interpolate using scipy wrappers """

        inplace = validate_bool_kwarg(inplace, 'inplace')
        data = self.values if inplace else self.values.copy()

        # only deal with floats
        if not self.is_float:
            if not self.is_integer:
                return self
            data = data.astype(np.float64)

        if fill_value is None:
            fill_value = self.fill_value

        if method in ('krogh', 'piecewise_polynomial', 'pchip'):
            if not index.is_monotonic:
                raise ValueError("{0} interpolation requires that the "
                                 "index be monotonic.".format(method))
        # process 1-d slices in the axis direction

        def func(x):

            # process a 1-d slice, returning it
            # should the axis argument be handled below in apply_along_axis?
            # i.e. not an arg to missing.interpolate_1d
            return missing.interpolate_1d(index, x, method=method, limit=limit,
                                          limit_direction=limit_direction,
                                          limit_area=limit_area,
                                          fill_value=fill_value,
                                          bounds_error=False, **kwargs)

        # interp each column independently
        interp_values = np.apply_along_axis(func, axis, data)

        blocks = [self.make_block_same_class(interp_values)]
        return self._maybe_downcast(blocks, downcast)
