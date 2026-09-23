    def setitem(self, indexer, value):
        """ set the value inplace; return a new block (of a possibly different
        dtype)

        indexer is a direct slice/positional indexer; value must be a
        compatible shape
        """

        # coerce None values, if appropriate
        if value is None:
            if self.is_numeric:
                value = np.nan

        # coerce args
        values, value = self._try_coerce_args(self.values, value)
        arr_value = np.array(value)

        # cast the values to a type that can hold nan (if necessary)
        if not self._can_hold_element(value):
            dtype, _ = com._maybe_promote(arr_value.dtype)
            values = values.astype(dtype)

        transf = (lambda x: x.T) if self.ndim == 2 else (lambda x: x)
        values = transf(values)
        l = len(values)

        # length checking
        # boolean with truth values == len of the value is ok too
        if isinstance(indexer, (np.ndarray, list)):
            if is_list_like(value) and len(indexer) != len(value):
                if not (isinstance(indexer, np.ndarray) and
                        indexer.dtype == np.bool_ and
                        len(indexer[indexer]) == len(value)):
                    raise ValueError("cannot set using a list-like indexer "
                                     "with a different length than the value")

        # slice
        elif isinstance(indexer, slice):

            if is_list_like(value) and l:
                if len(value) != _length_of_indexer(indexer, values):
                    raise ValueError("cannot set using a slice indexer with a "
                                     "different length than the value")

        try:
            # setting a single element for each dim and with a rhs that could be say a list
            # GH 6043
            if arr_value.ndim == 1 and (
                np.isscalar(indexer) or (isinstance(indexer, tuple) and all([ np.isscalar(idx) for idx in indexer ]))):
                values[indexer] = value

            # if we are an exact match (ex-broadcasting),
            # then use the resultant dtype
            elif len(arr_value.shape) and arr_value.shape[0] == values.shape[0] and np.prod(arr_value.shape) == np.prod(values.shape):
                values[indexer] = value
                values = values.astype(arr_value.dtype)

            # set
            else:
                values[indexer] = value

            # coerce and try to infer the dtypes of the result
            if np.isscalar(value):
                dtype, _ = _infer_dtype_from_scalar(value)
            else:
                dtype = 'infer'
            values = self._try_coerce_and_cast_result(values, dtype)
            block = make_block(transf(values),
                               ndim=self.ndim, placement=self.mgr_locs,
                               fastpath=True)

            # may have to soft convert_objects here
            if block.is_object and not self.is_object:
                block = block.convert(convert_numeric=False)

            return block
        except (ValueError, TypeError) as detail:
            raise
        except Exception as detail:
            pass

        return [self]
