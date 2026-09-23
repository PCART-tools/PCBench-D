    def _init_dict(self, data, index, columns, dtype=None):
        # pre-filter out columns if we passed it
        if columns is not None:
            columns = _ensure_index(columns)
            data = dict((k, v) for k, v in compat.iteritems(data)
                        if k in columns)
        else:
            columns = Index(_try_sort(list(data.keys())))

        if index is None:
            index = extract_index(list(data.values()))

        sp_maker = lambda x: SparseArray(x, kind=self._default_kind,
                                         fill_value=self._default_fill_value,
                                         copy=True, dtype=dtype)
        sdict = DataFrame()
        for k, v in compat.iteritems(data):
            if isinstance(v, Series):
                # Force alignment, no copy necessary
                if not v.index.equals(index):
                    v = v.reindex(index)

                if not isinstance(v, SparseSeries):
                    v = sp_maker(v.values)
            elif isinstance(v, SparseArray):
                v = v.copy()
            else:
                if isinstance(v, dict):
                    v = [v.get(i, nan) for i in index]

                v = sp_maker(v)
            sdict[k] = v

        # TODO: figure out how to handle this case, all nan's?
        # add in any other columns we want to have (completeness)
        nan_vec = np.empty(len(index))
        nan_vec.fill(nan)
        for c in columns:
            if c not in sdict:
                sdict[c] = sp_maker(nan_vec)

        return to_manager(sdict, columns, index)
