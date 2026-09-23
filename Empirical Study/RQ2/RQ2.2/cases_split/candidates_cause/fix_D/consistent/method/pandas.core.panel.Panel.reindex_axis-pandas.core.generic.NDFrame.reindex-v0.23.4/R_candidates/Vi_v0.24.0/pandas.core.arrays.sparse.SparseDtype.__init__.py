    def __init__(self, dtype=np.float64, fill_value=None):
        # type: (Union[str, np.dtype, 'ExtensionDtype', type], Any) -> None
        from pandas.core.dtypes.missing import na_value_for_dtype
        from pandas.core.dtypes.common import (
            pandas_dtype, is_string_dtype, is_scalar
        )

        if isinstance(dtype, type(self)):
            if fill_value is None:
                fill_value = dtype.fill_value
            dtype = dtype.subtype

        dtype = pandas_dtype(dtype)
        if is_string_dtype(dtype):
            dtype = np.dtype('object')

        if fill_value is None:
            fill_value = na_value_for_dtype(dtype)

        if not is_scalar(fill_value):
            raise ValueError("fill_value must be a scalar. Got {} "
                             "instead".format(fill_value))
        self._dtype = dtype
        self._fill_value = fill_value
