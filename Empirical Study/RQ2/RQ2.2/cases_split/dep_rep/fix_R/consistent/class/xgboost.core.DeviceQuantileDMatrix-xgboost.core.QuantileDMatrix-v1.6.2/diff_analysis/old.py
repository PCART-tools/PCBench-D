class DeviceQuantileDMatrix(DMatrix):
    """Device memory Data Matrix used in XGBoost for training with tree_method='gpu_hist'. Do
    not use this for test/validation tasks as some information may be lost in
    quantisation. This DMatrix is primarily designed to save memory in training from
    device memory inputs by avoiding intermediate storage. Set max_bin to control the
    number of bins during quantisation.  See doc string in :py:obj:`xgboost.DMatrix` for
    documents on meta info.

    You can construct DeviceQuantileDMatrix from cupy/cudf/dlpack.

    .. versionadded:: 1.1.0

    """

    @_deprecate_positional_args
    def __init__(  # pylint: disable=super-init-not-called
        self,
        data: DataType,
        label: Optional[ArrayLike] = None,
        *,
        weight: Optional[ArrayLike] = None,
        base_margin: Optional[ArrayLike] = None,
        missing: Optional[float] = None,
        silent: bool = False,
        feature_names: FeatureNames = None,
        feature_types: Optional[List[str]] = None,
        nthread: Optional[int] = None,
        max_bin: int = 256,
        group: Optional[ArrayLike] = None,
        qid: Optional[ArrayLike] = None,
        label_lower_bound: Optional[ArrayLike] = None,
        label_upper_bound: Optional[ArrayLike] = None,
        feature_weights: Optional[ArrayLike] = None,
        enable_categorical: bool = False,
    ) -> None:
        self.max_bin = max_bin
        self.missing = missing if missing is not None else np.nan
        self.nthread = nthread if nthread is not None else 1
        self._silent = silent  # unused, kept for compatibility

        if isinstance(data, ctypes.c_void_p):
            self.handle = data
            return

        if qid is not None and group is not None:
            raise ValueError(
                'Only one of the eval_qid or eval_group for each evaluation '
                'dataset should be provided.'
            )

        self._init(
            data,
            label=label,
            weight=weight,
            base_margin=base_margin,
            group=group,
            qid=qid,
            label_lower_bound=label_lower_bound,
            label_upper_bound=label_upper_bound,
            feature_weights=feature_weights,
            feature_names=feature_names,
            feature_types=feature_types,
            enable_categorical=enable_categorical,
        )

    def _init(self, data: DataType, enable_categorical: bool, **meta: Any) -> None:
        from .data import (
            _is_dlpack,
            _transform_dlpack,
            _is_iter,
            SingleBatchInternalIter,
        )

        if _is_dlpack(data):
            # We specialize for dlpack because cupy will take the memory from it so
            # it can't be transformed twice.
            data = _transform_dlpack(data)
        if _is_iter(data):
            it = data
        else:
            it = SingleBatchInternalIter(data=data, **meta)

        handle = ctypes.c_void_p()
        reset_callback, next_callback = it.get_callbacks(False, enable_categorical)
        if it.cache_prefix is not None:
            raise ValueError(
                "DeviceQuantileDMatrix doesn't cache data, remove the cache_prefix "
                "in iterator to fix this error."
            )
        ret = _LIB.XGDeviceQuantileDMatrixCreateFromCallback(
            None,
            it.proxy.handle,
            reset_callback,
            next_callback,
            ctypes.c_float(self.missing),
            ctypes.c_int(self.nthread),
            ctypes.c_int(self.max_bin),
            ctypes.byref(handle),
        )
        it.reraise()
        # delay check_call to throw intermediate exception first
        _check_call(ret)
        self.handle = handle
