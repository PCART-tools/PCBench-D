    def _dt_tz_localize(
        self,
        tz,
        ambiguous: TimeAmbiguous = "raise",
        nonexistent: TimeNonexistent = "raise",
    ):
        if ambiguous != "raise":
            raise NotImplementedError(f"{ambiguous=} is not supported")
        if nonexistent != "raise":
            raise NotImplementedError(f"{nonexistent=} is not supported")
        if tz is None:
            new_type = pa.timestamp(self.dtype.pyarrow_dtype.unit)
            return type(self)(self._data.cast(new_type))
        pa_tz = str(tz)
        return type(self)(
            self._data.cast(pa.timestamp(self.dtype.pyarrow_dtype.unit, pa_tz))
        )
