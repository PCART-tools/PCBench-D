    @_period_dispatch
    def _quantile(
        self: DatetimeLikeArrayT,
        qs: npt.NDArray[np.float64],
        interpolation: str,
    ) -> DatetimeLikeArrayT:
        return super()._quantile(qs=qs, interpolation=interpolation)
