    def __init__(self, data=None, index=None, sparse_index=None, kind='block',
                 fill_value=None, name=None, dtype=None, copy=False,
                 fastpath=False):

        # we are called internally, so short-circuit
        if fastpath:

            # data is an ndarray, index is defined

            if not isinstance(data, SingleBlockManager):
                data = SingleBlockManager(data, index, fastpath=True)
            if copy:
                data = data.copy()

        else:

            if data is None:
                data = []

            if isinstance(data, Series) and name is None:
                name = data.name

            if isinstance(data, SparseArray):
                if index is not None:
                    assert (len(index) == len(data))
                sparse_index = data.sp_index
                if fill_value is None:
                    fill_value = data.fill_value

                data = np.asarray(data)

            elif isinstance(data, SparseSeries):
                if index is None:
                    index = data.index.view()
                if fill_value is None:
                    fill_value = data.fill_value
                # extract the SingleBlockManager
                data = data._data

            elif isinstance(data, (Series, dict)):
                data = Series(data, index=index)
                index = data.index.view()

                res = make_sparse(data, kind=kind, fill_value=fill_value)
                data, sparse_index, fill_value = res

            elif isinstance(data, (tuple, list, np.ndarray)):
                # array-like
                if sparse_index is None:
                    res = make_sparse(data, kind=kind, fill_value=fill_value)
                    data, sparse_index, fill_value = res
                else:
                    assert (len(data) == sparse_index.npoints)

            elif isinstance(data, SingleBlockManager):
                if dtype is not None:
                    data = data.astype(dtype)
                if index is None:
                    index = data.index.view()
                else:

                    data = data.reindex(index, copy=False)

            else:
                length = len(index)

                if data == fill_value or (isna(data) and isna(fill_value)):
                    if kind == 'block':
                        sparse_index = BlockIndex(length, [], [])
                    else:
                        sparse_index = IntIndex(length, [])
                    data = np.array([])

                else:
                    if kind == 'block':
                        locs, lens = ([0], [length]) if length else ([], [])
                        sparse_index = BlockIndex(length, locs, lens)
                    else:
                        sparse_index = IntIndex(length, index)
                    v = data
                    data = np.empty(length)
                    data.fill(v)

            if index is None:
                index = com._default_index(sparse_index.length)
            index = _ensure_index(index)

            # create/copy the manager
            if isinstance(data, SingleBlockManager):

                if copy:
                    data = data.copy()
            else:

                # create a sparse array
                if not isinstance(data, SparseArray):
                    data = SparseArray(data, sparse_index=sparse_index,
                                       fill_value=fill_value, dtype=dtype,
                                       copy=copy)

                data = SingleBlockManager(data, index)

        generic.NDFrame.__init__(self, data)

        self.index = index
        self.name = name
