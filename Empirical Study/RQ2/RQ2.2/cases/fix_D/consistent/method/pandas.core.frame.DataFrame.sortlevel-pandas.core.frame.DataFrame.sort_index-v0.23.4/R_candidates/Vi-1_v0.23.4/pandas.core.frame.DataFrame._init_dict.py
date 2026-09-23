    def _init_dict(self, data, index, columns, dtype=None):
        """
        Segregate Series based on type and coerce into matrices.
        Needs to handle a lot of exceptional cases.
        """
        if columns is not None:
            arrays = Series(data, index=columns, dtype=object)
            data_names = arrays.index

            missing = arrays.isnull()
            if index is None:
                # GH10856
                # raise ValueError if only scalars in dict
                index = extract_index(arrays[~missing])
            else:
                index = _ensure_index(index)

            # no obvious "empty" int column
            if missing.any() and not is_integer_dtype(dtype):
                if dtype is None or np.issubdtype(dtype, np.flexible):
                    # 1783
                    nan_dtype = object
                else:
                    nan_dtype = dtype
                v = construct_1d_arraylike_from_scalar(np.nan, len(index),
                                                       nan_dtype)
                arrays.loc[missing] = [v] * missing.sum()

        else:
            keys = com._dict_keys_to_ordered_list(data)
            columns = data_names = Index(keys)
            arrays = [data[k] for k in keys]

        return _arrays_to_mgr(arrays, data_names, index, columns, dtype=dtype)
