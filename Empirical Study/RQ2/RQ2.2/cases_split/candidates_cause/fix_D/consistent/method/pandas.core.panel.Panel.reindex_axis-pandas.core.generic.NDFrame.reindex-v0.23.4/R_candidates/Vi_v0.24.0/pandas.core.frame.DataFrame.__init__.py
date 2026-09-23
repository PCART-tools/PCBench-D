    def __init__(self, data=None, index=None, columns=None, dtype=None,
                 copy=False):
        if data is None:
            data = {}
        if dtype is not None:
            dtype = self._validate_dtype(dtype)

        if isinstance(data, DataFrame):
            data = data._data

        if isinstance(data, BlockManager):
            mgr = self._init_mgr(data, axes=dict(index=index, columns=columns),
                                 dtype=dtype, copy=copy)
        elif isinstance(data, dict):
            mgr = init_dict(data, index, columns, dtype=dtype)
        elif isinstance(data, ma.MaskedArray):
            import numpy.ma.mrecords as mrecords
            # masked recarray
            if isinstance(data, mrecords.MaskedRecords):
                mgr = masked_rec_array_to_mgr(data, index, columns, dtype,
                                              copy)

            # a masked array
            else:
                mask = ma.getmaskarray(data)
                if mask.any():
                    data, fill_value = maybe_upcast(data, copy=True)
                    data.soften_mask()  # set hardmask False if it was True
                    data[mask] = fill_value
                else:
                    data = data.copy()
                mgr = init_ndarray(data, index, columns, dtype=dtype,
                                   copy=copy)

        elif isinstance(data, (np.ndarray, Series, Index)):
            if data.dtype.names:
                data_columns = list(data.dtype.names)
                data = {k: data[k] for k in data_columns}
                if columns is None:
                    columns = data_columns
                mgr = init_dict(data, index, columns, dtype=dtype)
            elif getattr(data, 'name', None) is not None:
                mgr = init_dict({data.name: data}, index, columns,
                                dtype=dtype)
            else:
                mgr = init_ndarray(data, index, columns, dtype=dtype,
                                   copy=copy)

        # For data is list-like, or Iterable (will consume into list)
        elif (isinstance(data, compat.Iterable)
              and not isinstance(data, string_and_binary_types)):
            if not isinstance(data, compat.Sequence):
                data = list(data)
            if len(data) > 0:
                if is_list_like(data[0]) and getattr(data[0], 'ndim', 1) == 1:
                    if is_named_tuple(data[0]) and columns is None:
                        columns = data[0]._fields
                    arrays, columns = to_arrays(data, columns, dtype=dtype)
                    columns = ensure_index(columns)

                    # set the index
                    if index is None:
                        if isinstance(data[0], Series):
                            index = get_names_from_index(data)
                        elif isinstance(data[0], Categorical):
                            index = ibase.default_index(len(data[0]))
                        else:
                            index = ibase.default_index(len(data))

                    mgr = arrays_to_mgr(arrays, columns, index, columns,
                                        dtype=dtype)
                else:
                    mgr = init_ndarray(data, index, columns, dtype=dtype,
                                       copy=copy)
            else:
                mgr = init_dict({}, index, columns, dtype=dtype)
        else:
            try:
                arr = np.array(data, dtype=dtype, copy=copy)
            except (ValueError, TypeError) as e:
                exc = TypeError('DataFrame constructor called with '
                                'incompatible data and dtype: {e}'.format(e=e))
                raise_with_traceback(exc)

            if arr.ndim == 0 and index is not None and columns is not None:
                values = cast_scalar_to_array((len(index), len(columns)),
                                              data, dtype=dtype)
                mgr = init_ndarray(values, index, columns,
                                   dtype=values.dtype, copy=False)
            else:
                raise ValueError('DataFrame constructor not properly called!')

        NDFrame.__init__(self, mgr, fastpath=True)
