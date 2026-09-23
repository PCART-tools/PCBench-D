    def setitem(self, indexer, value):
        """Set the value inplace, returning a a maybe different typed block.

        Parameters
        ----------
        indexer : tuple, list-like, array-like, slice
            The subset of self.values to set
        value : object
            The value being set

        Returns
        -------
        Block

        Notes
        -----
        `indexer` is a direct slice/positional indexer. `value` must
        be a compatible shape.
        """
        # coerce None values, if appropriate
        if value is None:
            if self.is_numeric:
                value = np.nan

        # coerce if block dtype can store value
        values = self.values
        try:
            values, value = self._try_coerce_args(values, value)
            # can keep its own dtype
            if hasattr(value, 'dtype') and is_dtype_equal(values.dtype,
                                                          value.dtype):
                dtype = self.dtype
            else:
                dtype = 'infer'

        except (TypeError, ValueError):
            # current dtype cannot store value, coerce to common dtype
            find_dtype = False

            if hasattr(value, 'dtype'):
                dtype = value.dtype
                find_dtype = True

            elif lib.is_scalar(value):
                if isna(value):
                    # NaN promotion is handled in latter path
                    dtype = False
                else:
                    dtype, _ = infer_dtype_from_scalar(value,
                                                       pandas_dtype=True)
                    find_dtype = True
            else:
                dtype = 'infer'

            if find_dtype:
                dtype = find_common_type([values.dtype, dtype])
                if not is_dtype_equal(self.dtype, dtype):
                    b = self.astype(dtype)
                    return b.setitem(indexer, value)

        # value must be storeable at this moment
        arr_value = np.array(value)

        # cast the values to a type that can hold nan (if necessary)
        if not self._can_hold_element(value):
            dtype, _ = maybe_promote(arr_value.dtype)
            values = values.astype(dtype)

        transf = (lambda x: x.T) if self.ndim == 2 else (lambda x: x)
        values = transf(values)

        # length checking
        check_setitem_lengths(indexer, value, values)

        def _is_scalar_indexer(indexer):
            # return True if we are all scalar indexers

            if arr_value.ndim == 1:
                if not isinstance(indexer, tuple):
                    indexer = tuple([indexer])
                    return any(isinstance(idx, np.ndarray) and len(idx) == 0
                               for idx in indexer)
            return False

        def _is_empty_indexer(indexer):
            # return a boolean if we have an empty indexer

            if is_list_like(indexer) and not len(indexer):
                return True
            if arr_value.ndim == 1:
                if not isinstance(indexer, tuple):
                    indexer = tuple([indexer])
                return any(isinstance(idx, np.ndarray) and len(idx) == 0
                           for idx in indexer)
            return False

        # empty indexers
        # 8669 (empty)
        if _is_empty_indexer(indexer):
            pass

        # setting a single element for each dim and with a rhs that could
        # be say a list
        # GH 6043
        elif _is_scalar_indexer(indexer):
            values[indexer] = value

        # if we are an exact match (ex-broadcasting),
        # then use the resultant dtype
        elif (len(arr_value.shape) and
              arr_value.shape[0] == values.shape[0] and
              np.prod(arr_value.shape) == np.prod(values.shape)):
            values[indexer] = value
            try:
                values = values.astype(arr_value.dtype)
            except ValueError:
                pass

        # set
        else:
            values[indexer] = value

        # coerce and try to infer the dtypes of the result
        values = self._try_coerce_and_cast_result(values, dtype)
        block = self.make_block(transf(values))
        return block
