    def _to_timedeltaarray(self) -> TimedeltaArray:
        """Convert a pyarrow duration typed array to a TimedeltaArray."""
        from pandas.core.arrays.timedeltas import TimedeltaArray

        pa_type = self._pa_array.type
        assert pa.types.is_duration(pa_type)
        np_dtype = np.dtype(f"m8[{pa_type.unit}]")
        np_array = self._pa_array.to_numpy()
        np_array = np_array.astype(np_dtype)
        return TimedeltaArray._simple_new(np_array, dtype=np_dtype)
