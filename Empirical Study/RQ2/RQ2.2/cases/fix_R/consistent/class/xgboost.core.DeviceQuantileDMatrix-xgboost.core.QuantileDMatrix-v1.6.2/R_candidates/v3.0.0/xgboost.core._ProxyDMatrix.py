class _ProxyDMatrix(DMatrix):
    """A placeholder class when DMatrix cannot be constructed (QuantileDMatrix,
    inplace_predict).

    """

    def __init__(self) -> None:  # pylint: disable=super-init-not-called
        self.handle = ctypes.c_void_p()
        _check_call(_LIB.XGProxyDMatrixCreate(ctypes.byref(self.handle)))

    def _ref_data_from_cuda_interface(self, data: DataType) -> None:
        """Reference data from CUDA array interface."""
        arrinf = cuda_array_interface(data)
        _check_call(_LIB.XGProxyDMatrixSetDataCudaArrayInterface(self.handle, arrinf))

    def _ref_data_from_cuda_columnar(self, data: DataType, cat_codes: list) -> None:
        """Reference data from CUDA columnar format."""
        from .data import _cudf_array_interfaces

        interfaces_str = _cudf_array_interfaces(data, cat_codes)
        _check_call(_LIB.XGProxyDMatrixSetDataCudaColumnar(self.handle, interfaces_str))

    def _ref_data_from_array(self, data: np.ndarray) -> None:
        """Reference data from numpy array."""
        _check_call(_LIB.XGProxyDMatrixSetDataDense(self.handle, array_interface(data)))

    def _ref_data_from_columnar(self, data: TransformedDf) -> None:
        """Reference data from a CPU DataFrame."""
        _check_call(
            _LIB.XGProxyDMatrixSetDataColumnar(self.handle, data.array_interface())
        )

    def _ref_data_from_csr(self, csr: scipy.sparse.csr_matrix) -> None:
        """Reference data from scipy csr."""
        _LIB.XGProxyDMatrixSetDataCSR(
            self.handle,
            array_interface(csr.indptr),
            array_interface(csr.indices),
            array_interface(csr.data),
            ctypes.c_size_t(csr.shape[1]),
        )
