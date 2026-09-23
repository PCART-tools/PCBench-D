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

        if is_numeric_dtype(values.dtype):
            values = com.ensure_float(values)
            is_numeric = True
        else:
            if issubclass(values.dtype.type, np.datetime64):
                raise Exception('Cython not able to handle this case')

            values = values.astype(object)
            is_numeric = False

        # will be filled in Cython function
        result = np.empty(out_shape, dtype=values.dtype)
        counts = np.zeros(self.ngroups, dtype=np.int64)

        result = self._aggregate(result, counts, values, how, is_numeric)

        if self._filter_empty_groups:
            if result.ndim == 2:
                if is_numeric:
                    result = lib.row_bool_subset(
                        result, (counts > 0).view(np.uint8))
                else:
                    result = lib.row_bool_subset_object(
                        result, (counts > 0).view(np.uint8))
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
