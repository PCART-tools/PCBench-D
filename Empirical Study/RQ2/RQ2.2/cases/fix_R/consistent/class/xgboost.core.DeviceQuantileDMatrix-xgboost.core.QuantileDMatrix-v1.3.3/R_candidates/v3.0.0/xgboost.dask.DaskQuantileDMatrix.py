class DaskQuantileDMatrix(DaskDMatrix):
    """A dask version of :py:class:`QuantileDMatrix`. See :py:class:`DaskDMatrix` for
    parameter documents.

    """

    @_deprecate_positional_args
    def __init__(
        self,
        client: Optional["distributed.Client"],
        data: _DataT,
        label: Optional[_DaskCollection] = None,
        *,
        weight: Optional[_DaskCollection] = None,
        base_margin: Optional[_DaskCollection] = None,
        missing: Optional[float] = None,
        silent: bool = False,  # disable=unused-argument
        feature_names: Optional[FeatureNames] = None,
        feature_types: Optional[Union[Any, List[Any]]] = None,
        max_bin: Optional[int] = None,
        ref: Optional[DaskDMatrix] = None,
        group: Optional[_DaskCollection] = None,
        qid: Optional[_DaskCollection] = None,
        label_lower_bound: Optional[_DaskCollection] = None,
        label_upper_bound: Optional[_DaskCollection] = None,
        feature_weights: Optional[_DaskCollection] = None,
        enable_categorical: bool = False,
        max_quantile_batches: Optional[int] = None,
    ) -> None:
        super().__init__(
            client=client,
            data=data,
            label=label,
            weight=weight,
            base_margin=base_margin,
            group=group,
            qid=qid,
            label_lower_bound=label_lower_bound,
            label_upper_bound=label_upper_bound,
            missing=missing,
            silent=silent,
            feature_weights=feature_weights,
            feature_names=feature_names,
            feature_types=feature_types,
            enable_categorical=enable_categorical,
        )
        self.max_bin = max_bin
        self.max_quantile_batches = max_quantile_batches
        self.is_quantile = True
        self._ref: Optional[int] = id(ref) if ref is not None else None

    def _create_fn_args(self, worker_addr: str) -> Dict[str, Any]:
        args = super()._create_fn_args(worker_addr)
        args["max_bin"] = self.max_bin
        args["max_quantile_batches"] = self.max_quantile_batches
        if self._ref is not None:
            args["ref"] = self._ref
        return args
