    @property
    def _dt_time(self):
        unit = (
            self.dtype.pyarrow_dtype.unit
            if self.dtype.pyarrow_dtype.unit in {"us", "ns"}
            else "ns"
        )
        return type(self)(self._data.cast(pa.time64(unit)))
