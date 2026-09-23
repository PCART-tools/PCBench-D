class DeviceQuantileDMatrix(DMatrix):
    """Device memory Data Matrix used in XGBoost for training with
    tree_method='gpu_hist'. Do not use this for test/validation tasks as some
    information may be lost in quantisation. This DMatrix is primarily designed
    to save memory in training from device memory inputs by avoiding
    intermediate storage. Set max_bin to control the number of bins during
    quantisation.

    You can construct DeviceQuantileDMatrix from cupy/cudf/dlpack.

    .. versionadded:: 1.1.0
    """

    def __init__(self, data, label=None, weight=None,  # pylint: disable=W0231
                 base_margin=None,
                 missing=None,
                 silent=False,
                 feature_names=None,
                 feature_types=None,
                 nthread=None, max_bin=256):
        self.max_bin = max_bin
        self.missing = missing if missing is not None else np.nan
        self.nthread = nthread if nthread is not None else 1

        if isinstance(data, ctypes.c_void_p):
            self.handle = data
            return
        from .data import init_device_quantile_dmatrix
        handle, feature_names, feature_types = init_device_quantile_dmatrix(
            data, missing=self.missing, threads=self.nthread,
            max_bin=self.max_bin,
            label=label, weight=weight,
            base_margin=base_margin,
            group=None,
            label_lower_bound=None,
            label_upper_bound=None,
            feature_names=feature_names,
            feature_types=feature_types)
        self.handle = handle

        self.feature_names = feature_names
        self.feature_types = feature_types

    def _set_data_from_cuda_interface(self, data):
        '''Set data from CUDA array interface.'''
        interface = data.__cuda_array_interface__
        interface_str = bytes(json.dumps(interface, indent=2), 'utf-8')
        _check_call(
            _LIB.XGDeviceQuantileDMatrixSetDataCudaArrayInterface(
                self.handle,
                interface_str
            )
        )

    def _set_data_from_cuda_columnar(self, data):
        '''Set data from CUDA columnar format.1'''
        from .data import _cudf_array_interfaces
        interfaces_str = _cudf_array_interfaces(data)
        _check_call(
            _LIB.XGDeviceQuantileDMatrixSetDataCudaColumnar(
                self.handle,
                interfaces_str
            )
        )
