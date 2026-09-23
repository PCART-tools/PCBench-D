    def __init__(
        self,
        data=None,
        index=None,
        sparse_index=None,
        kind="block",
        fill_value=None,
        name=None,
        dtype=None,
        copy=False,
        fastpath=False,
    ):
        warnings.warn(depr_msg, FutureWarning, stacklevel=2)
        # TODO: Most of this should be refactored and shared with Series
        # 1. BlockManager -> array
        # 2. Series.index, Series.name, index, name reconciliation
        # 3. Implicit reindexing
        # 4. Implicit broadcasting
        # 5. Dict construction
        if data is None:
            data = []
        elif isinstance(data, SingleBlockManager):
            index = data.index
            data = data.blocks[0].values
        elif isinstance(data, (ABCSeries, ABCSparseSeries)):
            index = data.index if index is None else index
            dtype = data.dtype if dtype is None else dtype
            name = data.name if name is None else name

            if index is not None:
                data = data.reindex(index)

        elif isinstance(data, abc.Mapping):
            data, index = Series()._init_dict(data, index=index)

        elif is_scalar(data) and index is not None:
            data = np.full(len(index), fill_value=data)

        super().__init__(
            SparseArray(
                data,
                sparse_index=sparse_index,
                kind=kind,
                dtype=dtype,
                fill_value=fill_value,
                copy=copy,
            ),
            index=index,
            name=name,
            copy=False,
            fastpath=fastpath,
        )
