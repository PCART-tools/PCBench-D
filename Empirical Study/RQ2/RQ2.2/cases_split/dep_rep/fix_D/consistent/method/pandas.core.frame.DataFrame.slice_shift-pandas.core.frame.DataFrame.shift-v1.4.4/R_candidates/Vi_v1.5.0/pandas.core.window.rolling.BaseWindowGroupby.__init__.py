    def __init__(
        self,
        obj: DataFrame | Series,
        *args,
        _grouper: BaseGrouper,
        _as_index: bool = True,
        **kwargs,
    ) -> None:
        from pandas.core.groupby.ops import BaseGrouper

        if not isinstance(_grouper, BaseGrouper):
            raise ValueError("Must pass a BaseGrouper object.")
        self._grouper = _grouper
        self._as_index = _as_index
        # GH 32262: It's convention to keep the grouping column in
        # groupby.<agg_func>, but unexpected to users in
        # groupby.rolling.<agg_func>
        obj = obj.drop(columns=self._grouper.names, errors="ignore")
        # GH 15354
        if kwargs.get("step") is not None:
            raise NotImplementedError("step not implemented for groupby")
        super().__init__(obj, *args, **kwargs)
