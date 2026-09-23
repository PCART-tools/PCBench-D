    def __init__(self, dtype: Dtype = np.float64, fill_value: Any = None) -> None:
        if isinstance(dtype, type(self)):
            if fill_value is None:
                fill_value = dtype.fill_value
            dtype = dtype.subtype

        from pandas.core.dtypes.common import (
            is_string_dtype,
            pandas_dtype,
        )
        from pandas.core.dtypes.missing import na_value_for_dtype

        dtype = pandas_dtype(dtype)
        if is_string_dtype(dtype):
            dtype = np.dtype("object")
        if not isinstance(dtype, np.dtype):
            # GH#53160
            raise TypeError("SparseDtype subtype must be a numpy dtype")

        if fill_value is None:
            fill_value = na_value_for_dtype(dtype)

        self._dtype = dtype
        self._fill_value = fill_value
        self._check_fill_value()
