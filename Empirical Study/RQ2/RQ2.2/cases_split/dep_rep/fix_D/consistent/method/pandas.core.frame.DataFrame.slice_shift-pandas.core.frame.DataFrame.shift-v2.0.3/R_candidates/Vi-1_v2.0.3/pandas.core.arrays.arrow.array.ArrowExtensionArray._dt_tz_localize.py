    def _dt_tz_localize(
        self,
        tz,
        ambiguous: TimeAmbiguous = "raise",
        nonexistent: TimeNonexistent = "raise",
    ):
        if ambiguous != "raise":
            raise NotImplementedError(f"{ambiguous=} is not supported")
        nonexistent_pa = {
            "raise": "raise",
            "shift_backward": "earliest",
            "shift_forward": "latest",
        }.get(
            nonexistent, None  # type: ignore[arg-type]
        )
        if nonexistent_pa is None:
            raise NotImplementedError(f"{nonexistent=} is not supported")
        if tz is None:
            result = self._data.cast(pa.timestamp(self.dtype.pyarrow_dtype.unit))
        else:
            result = pc.assume_timezone(
                self._data, str(tz), ambiguous=ambiguous, nonexistent=nonexistent_pa
            )
        return type(self)(result)
