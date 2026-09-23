    def _init_dict(self, data, index, columns, dtype=None):
        """
        Segregate Series based on type and coerce into matrices.
        Needs to handle a lot of exceptional cases.
        """
        if columns is not None:
            columns = _ensure_index(columns)

            # prefilter if columns passed

            data = dict((k, v) for k, v in compat.iteritems(data)
                        if k in columns)

            if index is None:
                index = extract_index(list(data.values()))
            else:
                index = _ensure_index(index)

            arrays = []
            data_names = []
            for k in columns:
                if k not in data:
                    # no obvious "empty" int column
                    if dtype is not None and issubclass(dtype.type,
                                                        np.integer):
                        continue

                    if dtype is None:
                        # 1783
                        v = np.empty(len(index), dtype=object)
                    else:
                        v = np.empty(len(index), dtype=dtype)

                    v.fill(NA)
                else:
                    v = data[k]
                data_names.append(k)
                arrays.append(v)
        else:
            keys = list(data.keys())
            if not isinstance(data, OrderedDict):
                keys = _try_sort(list(data.keys()))
            columns = data_names = Index(keys)
            arrays = [data[k] for k in columns]

        return _arrays_to_mgr(arrays, data_names, index, columns,
                              dtype=dtype)
