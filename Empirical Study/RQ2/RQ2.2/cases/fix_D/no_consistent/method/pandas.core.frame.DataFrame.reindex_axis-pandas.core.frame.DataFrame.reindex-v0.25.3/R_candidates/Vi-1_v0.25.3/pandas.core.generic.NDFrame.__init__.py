    def __init__(
        self,
        data: BlockManager,
        axes: Optional[List[Index]] = None,
        copy: bool = False,
        dtype: Optional[Dtype] = None,
        fastpath: bool = False,
    ):

        if not fastpath:
            if dtype is not None:
                data = data.astype(dtype)
            elif copy:
                data = data.copy()

            if axes is not None:
                for i, ax in enumerate(axes):
                    data = data.reindex_axis(ax, axis=i)

        object.__setattr__(self, "_is_copy", None)
        object.__setattr__(self, "_data", data)
        object.__setattr__(self, "_item_cache", {})
