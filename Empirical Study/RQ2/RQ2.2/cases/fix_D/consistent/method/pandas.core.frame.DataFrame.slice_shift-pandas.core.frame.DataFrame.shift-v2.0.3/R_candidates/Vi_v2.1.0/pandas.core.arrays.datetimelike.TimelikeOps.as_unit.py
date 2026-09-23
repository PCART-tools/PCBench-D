    def as_unit(self, unit: str) -> Self:
        if unit not in ["s", "ms", "us", "ns"]:
            raise ValueError("Supported units are 's', 'ms', 'us', 'ns'")

        dtype = np.dtype(f"{self.dtype.kind}8[{unit}]")
        new_values = astype_overflowsafe(self._ndarray, dtype, round_ok=True)

        if isinstance(self.dtype, np.dtype):
            new_dtype = new_values.dtype
        else:
            tz = cast("DatetimeArray", self).tz
            new_dtype = DatetimeTZDtype(tz=tz, unit=unit)

        # error: Unexpected keyword argument "freq" for "_simple_new" of
        # "NDArrayBacked"  [call-arg]
        return type(self)._simple_new(
            new_values, dtype=new_dtype, freq=self.freq  # type: ignore[call-arg]
        )
