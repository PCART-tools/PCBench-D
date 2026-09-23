    def _quantile(
        self: PeriodArray,
        qs: npt.NDArray[np.float64],
        interpolation: str,
    ) -> PeriodArray:
        # dispatch to DatetimeArray implementation
        dtres = self.view("M8[ns]")._quantile(qs, interpolation)
        # error: Incompatible return value type (got "Union[ExtensionArray,
        # ndarray[Any, Any]]", expected "PeriodArray")
        return dtres.view(self.dtype)  # type: ignore[return-value]
