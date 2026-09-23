    def aggregate(self, values, how, axis=0):
        arity = self._cython_arity.get(how, 1)

        vdim = values.ndim
        swapped = False
        if vdim == 1:
            values = values[:, None]
            out_shape = (self.ngroups, arity)
        else:
            if axis > 0:
                swapped = True
                values = values.swapaxes(0, axis)
            if arity > 1:
                raise NotImplementedError
            out_shape = (self.ngroups,) + values.shape[1:]

        is_numeric = is_numeric_dtype(values.dtype)

        if is_datetime_or_timedelta_dtype(values.dtype):
            values = values.view('int64')
        elif is_bool_dtype(values.dtype):
            values = _algos.ensure_float64(values)
        elif com.is_integer_dtype(values):
            values = values.astype('int64', copy=False)
        elif is_numeric:
            values = _algos.ensure_float64(values)
        else:
            values = values.astype(object)

        try:
            agg_func, dtype_str = self._get_aggregate_function(how, values)
        except NotImplementedError:
            if is_numeric:
                values = _algos.ensure_float64(values)
                agg_func, dtype_str = self._get_aggregate_function(how, values)
            else:
                raise

        if is_numeric:
            out_dtype = '%s%d' % (values.dtype.kind, values.dtype.itemsize)
        else:
            out_dtype = 'object'

        # will be filled in Cython function
        result = np.empty(out_shape, dtype=out_dtype)
        result.fill(np.nan)
        counts = np.zeros(self.ngroups, dtype=np.int64)

        result = self._aggregate(result, counts, values, agg_func, is_numeric)

        if com.is_integer_dtype(result):
            if len(result[result == tslib.iNaT]) > 0:
                result = result.astype('float64')
                result[result == tslib.iNaT] = np.nan

        if self._filter_empty_groups and not counts.all():
            if result.ndim == 2:
                try:
                    result = lib.row_bool_subset(
                        result, (counts > 0).view(np.uint8))
                except ValueError:
                    result = lib.row_bool_subset_object(
                                    com._ensure_object(result),
                                    (counts > 0).view(np.uint8))
            else:
                result = result[counts > 0]

        if vdim == 1 and arity == 1:
            result = result[:, 0]

        if how in self._name_functions:
            # TODO
            names = self._name_functions[how]()
        else:
            names = None

        if swapped:
            result = result.swapaxes(0, axis)

        return result, names
