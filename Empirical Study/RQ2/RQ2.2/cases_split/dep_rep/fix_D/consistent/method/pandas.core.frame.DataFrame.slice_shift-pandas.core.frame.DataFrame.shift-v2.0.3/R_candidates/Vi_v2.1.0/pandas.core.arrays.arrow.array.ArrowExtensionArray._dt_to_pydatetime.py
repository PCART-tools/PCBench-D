    def _dt_to_pydatetime(self):
        if pa.types.is_date(self.dtype.pyarrow_dtype):
            raise ValueError(
                f"to_pydatetime cannot be called with {self.dtype.pyarrow_dtype} type. "
                "Convert to pyarrow timestamp type."
            )
        data = self._pa_array.to_pylist()
        if self._dtype.pyarrow_dtype.unit == "ns":
            data = [None if ts is None else ts.to_pydatetime(warn=False) for ts in data]
        return np.array(data, dtype=object)
