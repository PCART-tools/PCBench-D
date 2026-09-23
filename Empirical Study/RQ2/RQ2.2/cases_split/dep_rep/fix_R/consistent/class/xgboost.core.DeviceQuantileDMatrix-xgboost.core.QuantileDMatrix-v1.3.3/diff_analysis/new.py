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
        data,
        label=None,
        *,
        weight=None,
        base_margin=None,
        missing=None,
        silent=False,
        feature_names=None,
        feature_types=None,
        nthread: Optional[int] = None,
        max_bin: int = 256,
        group=None,
        qid=None,
        label_lower_bound=None,
        label_upper_bound=None,
        feature_weights=None,
        enable_categorical: bool = False,
    ):
        self.max_bin = max_bin
        self.missing = missing if missing is not None else np.nan
        self.nthread = nthread if nthread is not None else 1
        self._silent = silent  # unused, kept for compatibility

        if isinstance(data, ctypes.c_void_p):
            self.handle = data
            return

        if enable_categorical:
            raise NotImplementedError(
                'categorical support is not enabled on DeviceQuantileDMatrix.'
            )
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
        )

    def _init(self, data, feature_names, feature_types, **meta):
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
            it = SingleBatchInternalIter(
                data, **meta, feature_names=feature_names, feature_types=feature_types
            )

        reset_callback = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(it.reset_wrapper)
        next_callback = ctypes.CFUNCTYPE(
            ctypes.c_int,
            ctypes.c_void_p,
        )(it.next_wrapper)
        handle = ctypes.c_void_p()
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
        if it.exception is not None:
            #  pylint 2.7.0 believes `it.exception` can be None even with `assert
            #  isinstace`
            raise it.exception  # pylint: disable=raising-bad-type
        # delay check_call to throw intermediate exception first
        _check_call(ret)
        self.handle = handle
