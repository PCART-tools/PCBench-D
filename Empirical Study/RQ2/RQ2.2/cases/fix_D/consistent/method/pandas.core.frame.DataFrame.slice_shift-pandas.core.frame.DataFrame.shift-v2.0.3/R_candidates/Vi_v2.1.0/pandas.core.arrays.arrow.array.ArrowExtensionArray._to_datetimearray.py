    def _to_datetimearray(self) -> DatetimeArray:
        """Convert a pyarrow timestamp typed array to a DatetimeArray."""
        from pandas.core.arrays.datetimes import (
            DatetimeArray,
            tz_to_dtype,
        )

        pa_type = self._pa_array.type
        assert pa.types.is_timestamp(pa_type)
        np_dtype = np.dtype(f"M8[{pa_type.unit}]")
        dtype = tz_to_dtype(pa_type.tz, pa_type.unit)
        np_array = self._pa_array.to_numpy()
        np_array = np_array.astype(np_dtype)
        return DatetimeArray._simple_new(np_array, dtype=dtype)
