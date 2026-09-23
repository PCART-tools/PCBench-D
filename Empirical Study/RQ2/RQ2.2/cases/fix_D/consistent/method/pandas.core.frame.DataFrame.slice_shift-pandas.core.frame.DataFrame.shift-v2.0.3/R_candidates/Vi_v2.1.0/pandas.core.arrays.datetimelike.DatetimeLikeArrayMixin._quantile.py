    @_period_dispatch
    def _quantile(
        self,
        qs: npt.NDArray[np.float64],
        interpolation: str,
    ) -> Self:
        return super()._quantile(qs=qs, interpolation=interpolation)
